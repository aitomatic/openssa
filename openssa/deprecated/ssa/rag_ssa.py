import json
from json import JSONDecodeError
from openssa.core.adapter.base_adapter import BaseAdapter
from openssa.core.slm.abstract_slm import AbstractSLM
from openssa.core.ssm.base_ssm import BaseSSM
from openssa.core.backend.rag_backend import AbstractRAGBackend
from openssa.core.slm.base_slm import PassthroughSLM
from openssa.core.prompts import Prompts
from openssa.utils.logs import Logs


class RAGSSM(BaseSSM):
    def __init__(self,
                 slm: AbstractSLM = None,
                 rag_backend: AbstractRAGBackend = None,
                 name: str = None,
                 storage_dir: str = None):
        """
        @param slm: The SLM to use.
        @param rag_backend: The RAG backend to use.
        @param name: The name of the SSM.
        @param storage_dir: The storage directory to use.
        """
        slm = slm or PassthroughSLM()
        self._rag_backend = rag_backend
        backends = [self.rag_backend] if self.rag_backend else None
        adapter = BaseAdapter(backends=backends)

        if self._rag_backend is not None and storage_dir is not None:
            self._rag_backend.load_index_if_exists(storage_dir)

        super().__init__(slm=slm, adapter=adapter, backends=backends, name=name, storage_dir=storage_dir)

    def is_passthrough(self) -> bool:
        return isinstance(self.slm, PassthroughSLM)

    @property
    def rag_backend(self) -> AbstractRAGBackend:
        return self._rag_backend

    def read_directory(self, storage_dir: str = None, re_index: bool = False):
        self.storage_dir = storage_dir or self.storage_dir
        self.rag_backend.read_directory(self.storage_dir, re_index)

    def read_gdrive(self, folder_id: str, storage_dir: str = None, re_index: bool = False):
        self.storage_dir = storage_dir or self.storage_dir
        self.rag_backend.read_gdrive(folder_id, self.storage_dir, re_index)

    def read_website(self, urls: list[str], storage_dir: str = None, re_index: bool = False):
        self.storage_dir = storage_dir or self.storage_dir
        self.rag_backend.read_website(urls, self.storage_dir, re_index)

    @Logs.do_log_entry_and_exit()
    def _make_conversation(self, user_input: list[dict], rag_response: list[dict]) -> list[dict]:
        """
        Combines the user input and the RAG response into a single input.
        The user_input looks like this:
        [{"role": "user", "content": "What is the capital of Spain?"}]

        while the rag_response looks like this:
        [{"response": "Madrid is the capital of Spain."},]

        We want the combined conversation to look like this:
        [
            {"role": "system", "content": "<instructions>"},
            {"role": "user", "content": "<user question>"},
            {"role": "assistant1", "content": "<rag response>"}
        ]
        """
        system_instructions = Prompts.make_prompt(
            __name__, "_make_conversation", "system")

        if isinstance(user_input, list):
            user_input = user_input[0]
            if "content" in user_input:
                user_input = user_input["content"]
        user_input = str(user_input)

        if isinstance(rag_response, list):
            rag_response = rag_response[0]
        if isinstance(rag_response, dict):
            if "content" in rag_response:
                rag_response = rag_response["content"]
            elif "response" in rag_response:
                rag_response = rag_response["response"]
        rag_response = str(rag_response)

        combined_user_input = Prompts.make_prompt(
            __name__, "_make_conversation", "user",
            user_input=user_input, rag_response=rag_response)

        return [
            {"role": "system", "content": system_instructions},
            {"role": "user", "content": combined_user_input},
        ]

    @Logs.do_log_entry_and_exit()
    def custom_discuss(self, user_input: list[dict], conversation: list[dict]) -> tuple[dict, list[dict]]:
        """
        An SSM with a RAG backend will reason between its own SLM’s knowledge
        and the knowledge of the RAG backend, before return the response.
        The process proceeds as follows:

        1. We first queries the RAG backend for a response.
        2. We then query the SLM for its response
        3. We combine the two responses into a single query to the SLM
        3. The SLM’s response is then returned.
        """
        # First get the RAG response.
        rag_response = None
        if self.rag_backend is not None:
            # rag_response should look like this:
            # {"response": "Madrid is the capital of Spain.", response_object: <RAGResponse>}
            rag_response = self.rag_backend.query(user_input, conversation)

        if isinstance(self.slm, PassthroughSLM):
            # We’re done if the SLM is a passthrough.
            if rag_response is None:
                return {"role": "assistant", "content": "No response."}, user_input

            if "response" not in rag_response:
                return {"role": "assistant", "content": rag_response}, user_input

            return {"role": "assistant", "content": rag_response["response"]}, user_input

        # Get the initial SLM response.
        slm_response = self.slm.do_discuss(user_input, conversation)

        if rag_response is None:
            # If there is no RAG response, then we’re done.
            return slm_response, user_input

        # Combine the user_input, rag_response, and slm_response into a single input,
        # and ask the SLM again with that combined input.
        combined_input = Prompts.make_prompt(
            __name__, "discuss", "combined_input",
            user_input=user_input[0]["content"],
            rag_response=rag_response,
            slm_response=slm_response)

        slm_response = self.slm.do_discuss(combined_input, conversation) # user_input is already in the conversation

        return slm_response, combined_input

    def _sanitize_rag_response(self, response) -> dict:
        # The response may be nested like so:
        # [{"role": "assistant", "content": "[{'role': 'assistant', 'details': 'xxx', 'content': 'What is the capital of Spain?'}]"}]
        # So we need to check for that and extract the content.
        if isinstance(response, list):
            response = response[0]

        if isinstance(response, dict):
            temp = response
            if "content" in temp:
                if isinstance(temp, dict):
                    temp = temp["content"]
                else:
                    temp = temp.content

                if isinstance(temp, list):
                    temp = temp[0]

                if isinstance(temp, dict):
                    # {"role": "assistant", "content": "What is the capital of Spain?"}
                    if "content" in temp:
                        response = temp
                elif isinstance(temp, str):
                    # "{\"role\": \"assistant\", \"content\": \"What is the capital of Spain?\"}}"
                    try:
                        response = json.loads(temp)
                    # pylint: disable=unused-variable
                    # flake8: noqa: F841
                    except JSONDecodeError as ex:
                        response = temp

        return response
