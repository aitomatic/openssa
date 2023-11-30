import os
from typing import Callable
from abc import abstractmethod, ABC
from openssa.core.backend.base_backend import BaseBackend
from openssa.utils.logs import Logs
from openssa.utils.utils import Utils


class AbstractRAGBackend(BaseBackend, ABC):
    def _get_source_dir(self, storage_dir: str):
        # return os.path.join(storage_dir, ".sources")
        if storage_dir is None:
            storage_dir = './'
        return os.path.abspath(storage_dir)

    def _get_index_dir(self, storage_dir: str):
        if storage_dir is None:
            storage_dir = './'
        return os.path.abspath(os.path.join(storage_dir, ".indexes"))

    def load_index_if_exists(self, storage_dir: str) -> bool:
        """
        Attempt to load an existing index from the storage directory.
        Returns True if an index was loaded, False otherwise.

        @param storage_dir: The path to the base storage directory.
        """
        index_dir = self._get_index_dir(storage_dir)
        if os.path.isdir(index_dir) and len(os.listdir(index_dir)) != 0:
            self.load(storage_dir)
            return True

        return False

    @abstractmethod
    def _do_read_directory(self, storage_dir: str):
        """
        Must be implemented by subclasses.

        @param storage_dir: The path to the base storage directory.
        """
        pass

    @abstractmethod
    def _do_read_website(self, urls: list[str], storage_dir: str):
        """
        Must be implemented by subclasses.

        @param url: The URL of the website to read.
        @param storage_dir: The path to the base storage directory.
        """
        pass

    @Logs.do_log_entry_and_exit()
    def _do_read_with_lambda(self,
                             reading_lambda: Callable,
                             storage_dir: str,
                             re_index: bool = False) -> bool:
        success = False

        if not re_index:
            success = self.load_index_if_exists(storage_dir)

        if not success or re_index:
            reading_lambda()
            # Side effect: save the index to the storage directory
            self.save(storage_dir)
            success = True

        return success

    def read_directory(self, storage_dir: str, re_index: bool = False) -> bool:
        """
        Read a directory of documents and create an index.

        @param storage_dir: The path to the base storage directory.
        @param re_index: [optional] If True, re-index the directory even if an index already exists.
        """
        self._do_read_with_lambda(lambda: self._do_read_directory(storage_dir),
                                  storage_dir,
                                  re_index)

    def _do_read_gdrive(self, folder_id: str, storage_dir: str) -> bool:
        Utils.download_gdrive(folder_id, self._get_source_dir(storage_dir))
        self._do_read_directory(storage_dir)

    def _do_read_s3(self, s3_paths: str | set[str], storage_dir: str) -> bool:
        Utils.download_s3(s3_paths, self._get_source_dir(storage_dir))
        self._do_read_directory(storage_dir)

    def read_gdrive(self, folder_id: str, storage_dir: str, re_index: bool = False):
        """
        Read a directory of documents from a Google Drive folder and create an index.
        Internally, the documents will first be downloaded to a local directory.

        @param folder_id: The ID of the Google Drive folder.
        @param storage_dir: The path to the base storage directory.
        @param re_index: [optional] If True, re-index the directory even if an index already exists.
        """
        self._do_read_with_lambda(lambda: self._do_read_gdrive(folder_id, storage_dir),
                                  storage_dir,
                                  re_index)

    def read_s3(self, s3_paths: str | set[str], storage_dir: str, use_existing_index: bool = True):
        """
        Read a directory of documents from an S3 folder and create an index.
        Internally, the documents will first be downloaded to a local directory.
        @param s3_dir: The path of the S3 folder.
        @param storage_dir: The path to the base storage directory.
        @param use_existing_index: [optional] If True, try to load an existing index from the storage directory first.
        Side effects:
        - If use_existing_index is True, the index will be automatically saved (for future use)
        """
        self._do_read_with_lambda(lambda: self._do_read_s3(s3_paths, storage_dir),
                                  storage_dir,
                                  use_existing_index)

    def read_website(self, urls: list[str], storage_dir: str, re_index: bool = False):
        """
        Read a directory of documents from a website and create an index.
        Internally, no documents are downloaded to a local directory.

        @param url: The URL of the website.
        @param storage_dir: The path to the base storage directory.
        @param re_index: [optional] If True, re-index the directory even if an index already exists.
        """
        self._do_read_with_lambda(lambda: self._do_read_website(urls, storage_dir),
                                  storage_dir,
                                  re_index)

    @abstractmethod
    def _do_save(self, storage_dir: str):
        """
        Must be implemented by subclasses.

        @param storage_dir: The path to the base storage directory.
        """
        pass

    def save(self, storage_dir: str):
        """
        Save the index to the storage directory.

        @param storage_dir: The path to the base storage directory.
        """
        self._do_save(storage_dir)
        return super().save(storage_dir)

    @abstractmethod
    def _do_load(self, storage_dir: str):
        """
        Must be implemented by subclasses.

        @param storage_dir: The path to the base storage directory.
        """
        pass

    def load(self, storage_dir: str):
        """
        Load the index from the storage directory.

        @param storage_dir: The path to the base storage directory.
        """
        self._do_load(storage_dir)
        return super().load(storage_dir)
