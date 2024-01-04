from llama_index.core import BaseQueryEngine, BaseRetriever


class RagResource:
    def __init__(self, query_engine: BaseQueryEngine, retriever: BaseRetriever) -> None:
        self.query_engine = query_engine
        self.retriever = retriever
