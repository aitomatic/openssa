import os
from llama_index.core import SimpleDirectoryReader
from llama_index.llms.openai import OpenAI
from openssa.utils.utils import Utils
from llama_index.core import StorageContext, load_index_from_storage, ServiceContext
from llama_index.core.retrievers import RecursiveRetriever
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.core.node_parser import SentenceSplitter
from openssa.core.rag_ooda.resources.dense_x.base import (
    DenseXRetrievalPack,
    load_nodes_dict,
    store_nodes_dict,
)
from openssa.core.rag_ooda.resources.rag_resource import RagResource


@Utils.timeit
def load_dense_x(data_dir: str, cache_dir: str, nodes_cache_path: str) -> RagResource:
    if (
        cache_dir is not None
        and os.path.exists(cache_dir)
        and os.path.exists(nodes_cache_path)
    ):
        service_context = ServiceContext.from_defaults(
            llm=OpenAI(model="gpt-4-1106-preview")
        )
        storage_context = StorageContext.from_defaults(persist_dir=cache_dir)
        vector_index = load_index_from_storage(storage_context)
        nodes = load_nodes_dict(nodes_cache_path)
        retriever = RecursiveRetriever(
            "vector",
            retriever_dict={"vector": vector_index.as_retriever(similarity_top_k=10)},
            node_dict=nodes,
        )

        query_engine = RetrieverQueryEngine.from_args(
            retriever, service_context=service_context
        )

    else:
        documents = SimpleDirectoryReader(data_dir).load_data()
        dense_pack = DenseXRetrievalPack(
            documents,
            proposition_llm=OpenAI(model="gpt-3.5-turbo", max_tokens=750),
            query_llm=OpenAI(model="gpt-4-1106-preview", max_tokens=1024),
            text_splitter=SentenceSplitter(chunk_size=1024),
        )
        store_nodes_dict(dense_pack.all_nodes_dict, nodes_cache_path)
        dense_pack.vector_index.storage_context.persist(cache_dir)
        retriever = dense_pack.retriever
        query_engine = dense_pack.query_engine
    return RagResource(query_engine=query_engine, retriever=retriever)
