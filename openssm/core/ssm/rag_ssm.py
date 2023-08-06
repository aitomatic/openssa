from openssm.core.adapter.base_adapter import BaseAdapter
from openssm.core.slm.abstract_slm import AbstractSLM
from openssm.core.ssm.base_ssm import BaseSSM
from openssm.core.backend.rag_backend import AbstractRAGBackend
from openssm.core.slm.base_slm import PassthroughSLM
from openssm.utils.prompts import Prompts
from openssm.utils.logs import Logs
from openssm.utils.utils import Utils


class RAGSSM(BaseSSM):
    rag_backend: AbstractRAGBackend = None

    def __init__(self,
                 slm: AbstractSLM = None,
                 rag_backend: AbstractRAGBackend = None,
                 name: str = None):
        slm = slm or PassthroughSLM()
        self.rag_backend = rag_backend
        backends = [self.rag_backend] if self.rag_backend else None
        adapter = BaseAdapter(backends=backends)
        super().__init__(slm=slm, adapter=adapter, backends=backends, name=name)

    def is_passthrough(self) -> bool:
        return isinstance(self.slm, PassthroughSLM)

    def get_rag_backend(self) -> AbstractRAGBackend:
        return self.rag_backend

    def read_directory(self, storage_dir: str = None, use_existing_index: bool = False):
        storage_dir = storage_dir or self._default_storage_dir
        self.get_rag_backend().read_directory(storage_dir, use_existing_index)

    def read_gdrive(self, folder_id: str, storage_dir: str = None, use_existing_index: bool = False):
        storage_dir = storage_dir or self._default_storage_dir
        self.get_rag_backend().read_gdrive(folder_id, storage_dir, use_existing_index)

    @Logs.do_log_entry_and_exit()
    def _combine_inputs(self, user_input: list[dict], rag_response: list[dict]) -> list[dict]:
        """
        Combines the user input and the RAG response into a single input.
        The user_input looks like this:
        [
            {"role": "user", "text": "What is the capital of Spain?"},
        ]

        while the rag_response looks like this:
        [
            {"role": "assistant", "text": "Madrid is the capital of Spain."},
        ]

        We want the combination to look like this:
        [
            {"role": "user", "content":
                "Answer the following (Question), by combining your own knowledge "
                "with that provided by a document-backed model (RAG), taking into account "
                "the fact that both you and the RAG model are imperfect, with possible "
                "hallucination. Do the best you can: "
                "Question: {user_input} (e.g., What is the capital of Spain?) "
                "RAG: {rag_response} (e.g., Madrid) "
            },
        ]
        """
        if isinstance(user_input, list):
            user_input = user_input[0]
            if "content" in user_input:
                user_input = user_input["content"]
        user_input = str(user_input)

        if isinstance(rag_response, list):
            rag_response = rag_response[0]
            if "content" in rag_response:
                rag_response = rag_response["content"]
        rag_response = str(rag_response)

        content_template = Prompts.get_module_prompt(__name__, "_combine_inputs")
        content = content_template.format(user_input=user_input, rag_response=rag_response)
        return [{"role": "user", "content": content}]

    @Utils.do_canonicalize_user_input_and_query_response('user_input')
    @Logs.do_log_entry_and_exit()
    def discuss(self, user_input: list[dict], conversation_id: str = None) -> list[dict]:
        """
        An SSM with a RAG backend will reason between its own SLM’s knowledge
        and the knowledge of the RAG backend, before return the response.
        The process proceeds as follows:

        1. It first queries the RAG backend for a response.
        2. It then queries the SLM, providing the initial query, as well as the
        response from the RAG backend as additional context.
        3. The SLM’s response is then returned.
        """
        rag_response = None

        if self.get_rag_backend() is not None:
            rag_response = self.get_rag_backend().query(user_input, conversation_id)

        if isinstance(self.slm, PassthroughSLM):
            return rag_response

        if rag_response is not None:
            user_input = self._combine_inputs(user_input, rag_response)

        result = self.slm.discuss(user_input, conversation_id)
        return result
