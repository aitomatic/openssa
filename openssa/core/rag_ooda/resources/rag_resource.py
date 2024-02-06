from llama_index.retrievers import BaseRetriever
from llama_index.query_engine import BaseQueryEngine


class RagResource:
    def __init__(self, query_engine: BaseQueryEngine, retriever: BaseRetriever) -> None:
        self.query_engine = query_engine
        self.retriever = retriever
