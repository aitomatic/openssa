import os.path
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, StorageContext, load_index_from_storage
from openssa.core.rag_ooda.resources.rag_resource import RagResource
from openssa.utils.utils import Utils


@Utils.timeit
def load_standard_vi(data_dir: str, cache_dir: str) -> RagResource:
    if not os.path.exists(cache_dir):
        documents = SimpleDirectoryReader(data_dir).load_data()
        index = VectorStoreIndex.from_documents(documents)
        index.storage_context.persist(cache_dir)
    else:
        storage_context = StorageContext.from_defaults(persist_dir=cache_dir)
        index = load_index_from_storage(storage_context)
    query_engine = index.as_query_engine()
    retriever = index.as_retriever()
    return RagResource(query_engine=query_engine, retriever=retriever)
