from dataclasses import dataclass
from llama_index import (
    download_loader,
    load_index_from_storage,
    SimpleDirectoryReader,
    VectorStoreIndex,
    Response,
    ServiceContext
)
from llama_index.indices.base import BaseIndex
from llama_index.indices.query.base import BaseQueryEngine
from llama_index.storage import StorageContext
from openssm.core.backend.rag_backend import AbstractRAGBackend


@dataclass
class Backend(AbstractRAGBackend):
    def __init__(self, relevance_threshold: float = 0.5):
        """
        Initialize the backend.

        @param relevance_threshold: The relevance threshold for the MMR query engine.
        0-1 (default: 0.5) The higher the threshold, the stricter the document relevance requirement.
        Increasing the threshold increases the relevance, but also decreases the chance
        of finding an answer.
        """
        self._index = None
        self._query_engine = None
        self._relevance_threshold = relevance_threshold
        super().__init__()

    @property
    def index(self) -> BaseIndex:
        return self._index

    @index.setter
    def index(self, index: BaseIndex):
        self._index = index

    @property
    def query_engine(self) -> BaseQueryEngine:
        if self._query_engine is None:
            if self.index is None:
                return None
            self._query_engine = self.index.as_query_engine(
                vector_store_query_mode="mmr",
                vector_store_kwargs={"mmr_threshold": self._relevance_threshold}
            )
        return self._query_engine

    @query_engine.setter
    def query_engine(self, query_engine: BaseQueryEngine):
        self._query_engine = query_engine

    # pylint: disable=unused-argument
    def query(self, user_input: list[dict], conversation: list[dict] = None) -> dict:
        """
        Query the index with the user input.

        Returns a tuple comprising (a) the response dicts and (b) the response object, if any.
        """
        response = None
        if self.query_engine is None:
            result = {"response": "I'm sorry, I don't have an index to query. Please load something first."}
        else:
            query = next((i['content'] for i in user_input if i['role'] == 'user'), None)
            response: Response = self.query_engine.query(query)
            if hasattr(response, "response"):
                result = {"response": response.response}
            elif isinstance(response, dict) and "response" in response:
                result = {"response": response["response"]}
            else:
                result = {"response": "I'm sorry, I don't have an answer for that."}

        return {"response": result, "response_object": response}

    def _create_index(self, documents):
        service_context = ServiceContext.from_defaults(chunk_size_limit=3000)
        self.index = VectorStoreIndex.from_documents(documents, service_context=service_context)

    def _do_read_directory(self, storage_dir: str):
        documents = SimpleDirectoryReader(self._get_source_dir(storage_dir)).load_data()
        self._create_index(documents)

    def _do_read_website(self, urls: list[str], storage_dir: str):
        the_class = download_loader("SimpleWebPageReader")
        loader = the_class()
        documents = loader.load_data(urls=urls)
        self._create_index(documents)

    def _do_save(self, storage_dir: str):
        self.index.storage_context.persist(persist_dir=self._get_index_dir(storage_dir))

    def _do_load(self, storage_dir: str):
        storage_context = StorageContext.from_defaults(persist_dir=self._get_index_dir(storage_dir))
        self.index = load_index_from_storage(storage_context)
