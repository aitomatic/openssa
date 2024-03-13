"""Query Rewriting Retriever Pack."""
from typing import Any, Dict

from llama_index.core import ServiceContext
from llama_index.core import VectorStoreIndex
from llama_index.core.llama_pack import BaseLlamaPack
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.core.retrievers import QueryFusionRetriever
from llama_index.core.retrievers.fusion_retriever import FUSION_MODES
from openssa.utils.rag_service_contexts import ServiceContextManager


class QueryRewritingRetrieverPack(BaseLlamaPack):
    """Query rewriting retriever pack.

    Rewrite the query into multiple queries and
    rerank the results.

    """

    def __init__(
        self,
        index: VectorStoreIndex = None,  # type: ignore
        chunk_size: int = 1024,
        vector_similarity_top_k: int = 5,
        fusion_similarity_top_k: int = 10,
        service_context: ServiceContext = None,
        **kwargs: Any,
    ) -> None:
        """Init params."""
        if not service_context:
            service_context = ServiceContextManager.get_openai_sc(chunk_size=chunk_size)
        self.vector_retriever = index.as_retriever(
            similarity_top_k=vector_similarity_top_k
        )

        self.fusion_retriever = QueryFusionRetriever(  # type: ignore
            [self.vector_retriever],
            similarity_top_k=fusion_similarity_top_k,
            num_queries=4,  # set this to 1 to disable query generation
            mode=FUSION_MODES.RECIPROCAL_RANK,
            use_async=True,
            verbose=True,
            # query_gen_prompt="...",
        )

        self.query_engine = RetrieverQueryEngine.from_args(
            self.fusion_retriever, service_context=service_context
        )

    def get_modules(self) -> Dict[str, Any]:
        """Get modules."""
        return {
            "vector_retriever": self.vector_retriever,
            "fusion_retriever": self.fusion_retriever,
            "query_engine": self.query_engine,
        }

    def retrieve(self, query_str: str) -> Any:
        """Retrieve."""
        return self.fusion_retriever.retrieve(query_str)

    def run(self, *args: Any, **kwargs: Any) -> Any:
        """Run the pipeline."""
        return self.query_engine.query(*args, **kwargs)
