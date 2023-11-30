"""Utilities."""


import functools
import inspect
import io
from itertools import chain
import json
import os
from pathlib import Path
import shutil
from typing import Any
from uuid import uuid4
import googleapiclient.errors
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from s3fs import S3FileSystem
from openssa.utils.fs import FileSource
from openssa.utils.logs import mlogger


class Utils:
    """Class containing various utility methods."""

    @staticmethod
    def canonicalize_user_input(user_input: Any) -> list[dict]:
        """
        Make sure user_input is in the form of a list of dicts,
        e.g., [{"role": "user", "content": "hello"}].
        """
        mlogger.debug("start: user_input: %s", user_input)

        if isinstance(user_input, list):
            # [{"role": "user", "content": "xxx"}, ...]
            results = []
            for item in user_input:
                if isinstance(item, dict) and "role" in item and "content" in item:
                    # {"role": "user", "content": "xxx"}
                    results.append(item)
                else:
                    # {"xxx": "yyy"} or any xxx
                    results.append({"role": "user", "content": str(item)})

            user_input = results

        elif isinstance(user_input, str):
            # "xxx"
            user_input = [{"role": "user", "content": user_input}]

        elif isinstance(user_input, dict):
            # {"role": "user", "content": "xxx"}
            user_input = [user_input]

        else:
            user_input = [{"role": "user", "content": str(user_input)}]

        mlogger.debug("end: user_input: %s", user_input)

        return user_input

    # pylint: disable=too-many-branches
    @staticmethod
    def canonicalize_discuss_result(result: Any) -> dict:
        """
        Make sure response is in the form of a dict,
        e.g., {"role": "assistant", "content": "hello"}.
        """
        if isinstance(result, tuple):
            # Take the first dict
            result = next((i for i in result if isinstance(i, dict)), None)

        if isinstance(result, dict):
            return Utils._handle_dict_output(result, "content", "response")

        if isinstance(result, list):
            return Utils._handle_list_output(result, "content", "response")

        if result is None:
            # No response
            return {"role": "assistant", "content": ""}

        if isinstance(result, str):
            return Utils._handle_str_output(result, True)

        # Any xxx
        return {"role": "assistant", "content": str(result).strip()}

    # pylint: disable=too-many-branches
    @staticmethod
    def canonicalize_query_response(response: Any) -> dict:
        """
        Make sure response is in the form of a dict
        e.g., {"response": "hello", "response_object": <obj>}
        """
        if isinstance(response, dict):
            return Utils._handle_dict_output(response, "response", "content")

        if isinstance(response, list):
            return Utils._handle_list_output(response, "response", "content")

        if response is None:
            return {"response": None, "response_object": None}

        if isinstance(response, str):
            return Utils._handle_str_output(response, False)

        # Any xxx
        return {"response": str(response).strip()}

    @staticmethod
    def _handle_str_output(result, is_discuss: bool) -> dict:
        result = result.strip()
        if (result.startswith("{") and result.endswith("}")) or (result.startswith("[") and result.endswith("]")):
            # {"role": "assistant", "content": "xxx"}
            # [{"role": "assistant", "content": "xxx"}, ...]
            try:
                return json.loads(result)
            except json.decoder.JSONDecodeError:
                pass

        if is_discuss:
            return {'role': 'assistant', 'content': result}
        return {'response': result}

    @staticmethod
    def _handle_dict_output(item: dict, required_key: str, alternate_key: str) -> dict:
        result = {}

        if required_key == "content":
            result["role"] = item["role"] if "role" in item else "assistant"

        if required_key in item:
            result[required_key] = item[required_key]
            return result

        if alternate_key in item:
            result[required_key] = item[alternate_key]
            return result

        result[required_key] = item
        return result

    @staticmethod
    def _handle_list_output(item: list, required_key: str, alternate_key: str) -> dict:
        if len(item) == 0:
            return {required_key: None}

        if len(item) == 1:
            item = item[0]
            if isinstance(item, dict):
                return Utils._handle_dict_output(item, required_key, alternate_key)
            if required_key == "content":
                return {"role": "assistant", "content": str(item).strip()}
            return {required_key: str(item).strip()}

        return {required_key: item}

    @staticmethod
    def do_canonicalize_user_input(param_name):
        """
        Decorator to canonicalize SSM user input.
        """
        def outer_decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                # Get the function signature
                sig = inspect.signature(func)
                param_names = list(sig.parameters.keys())
                if param_name not in param_names:
                    raise ValueError(f"Function does not have parameter named {param_name}")

                if param_name in kwargs:
                    # param_name is called as a keyword argument
                    kwargs[param_name] = Utils.canonicalize_user_input(kwargs[param_name])
                else:
                    # param_name is called as a positional argument
                    param_index = param_names.index(param_name)
                    args_list = list(args)
                    args_list[param_index] = Utils.canonicalize_user_input(args_list[param_index])
                    args = tuple(args_list)

                return func(*args, **kwargs)
            return wrapper
        return outer_decorator

    @staticmethod
    def do_canonicalize_discuss_result(func):
        """
        Decorator to canonicalize SSM discuss result.
        """
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)  # Execute the function first
            result = Utils.canonicalize_discuss_result(result)  # Modify the result
            return result
        return wrapper

    @staticmethod
    def do_canonicalize_query_response(func):
        """
        Decorator to canonicalize Backend query response.
        """
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            response = func(*args, **kwargs)  # Execute the function first
            response = Utils.canonicalize_query_response(response)  # Modify the response
            return response
        return wrapper

    @staticmethod
    def do_canonicalize_user_input_and_query_response(param_name):
        def outer_decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                decorated_func = Utils.do_canonicalize_user_input(param_name)(func)
                final_func = Utils.do_canonicalize_query_response(decorated_func)
                return final_func(*args, **kwargs)
            return wrapper
        return outer_decorator

    @staticmethod
    def do_canonicalize_user_input_and_discuss_result(param_name):
        def outer_decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                decorated_func = Utils.do_canonicalize_user_input(param_name)(func)
                final_func = Utils.do_canonicalize_discuss_result(decorated_func)
                return final_func(*args, **kwargs)
            return wrapper
        return outer_decorator

    @staticmethod
    def download_gdrive(folder_id: str, local_dir: str = './tmp/.docs'):
        try:
            creds_data = json.loads(os.getenv("GOOGLE_CREDENTIALS"))
            creds = Credentials.from_service_account_info(creds_data)
            service = build('drive', 'v3', credentials=creds)
            # pylint: disable=no-member
            results = service.files().list(q=f"'{folder_id}' in parents", pageSize=1000).execute()
            items = results.get('files', [])

            if not items:
                mlogger.info("No files found under Google Drive folder %s", folder_id)
                return

            mlogger.debug("Found %d files under Google Drive folder %s", len(items), folder_id)

            # Create local directory if it does not exist and clear it if it does
            if os.path.exists(local_dir):
                shutil.rmtree(local_dir)
            os.makedirs(local_dir)

            for item in items:
                request = service.files().get_media(fileId=item['id'])
                file_handle = io.FileIO(local_dir + '/' + item['name'], 'wb')
                downloader = MediaIoBaseDownload(file_handle, request)
                done = False
                while done is False:
                    status, done = downloader.next_chunk()
                    mlogger.debug("Downloading %s. Progress: %d%%.", item['name'], int(status.progress() * 100))

        except googleapiclient.errors.HttpError as error:
            mlogger.error("An error occurred: %s", error)

    _S3FS: S3FileSystem = None

    @staticmethod
    def download_s3(s3_paths: str | set[str], local_dir: str = './tmp/.docs'):
        if not Utils._S3FS:
            Utils._S3FS = S3FileSystem(key=os.environ.get('AWS_ACCESS_KEY_ID'),
                                       secret=os.environ.get('AWS_SECRET_ACCESS_KEY'))

        # Create local directory if it does not exist and clear it if it does
        if os.path.exists(local_dir):
            shutil.rmtree(local_dir)
        os.makedirs(local_dir)

        if isinstance(s3_paths, str):
            s3_paths: set[str] = {s3_paths}

        for s3_file_path in set(chain.from_iterable(FileSource(path=s3_path).file_paths(relative=False)
                                                    for s3_path in s3_paths)):
            # temp file path each document is copied to must retain same extension/suffix
            local_file_path: str = os.path.join(local_dir, f'{uuid4()}-{Path(s3_file_path).name}')

            Utils._S3FS.download(rpath=s3_file_path,
                                 lpath=local_file_path,
                                 recursive=False)
