from db_connector import MySQLDatabase
from llama_index.core.readers.file.base import SimpleDirectoryReader
from llama_index.core.indices.vector_store.base import VectorStoreIndex
from llama_index.core.schema import BaseNode, Document, IndexNode, TransformComponent
from llama_index.embeddings.openai.base import OpenAIEmbedding, OpenAIEmbeddingMode, OpenAIEmbeddingModelType
from multiprocessing import cpu_count

def create_index_from_data(table_data):
    documents = [Document(text=str(record)) for record in table_data]
    embed_model = OpenAIEmbedding(mode=OpenAIEmbeddingMode.SIMILARITY_MODE, model=OpenAIEmbeddingModelType.TEXT_EMBED_3_LARGE,
                           embed_batch_size=100, dimensions=3072, additional_kwargs=None,
                           api_key=None, api_base=None, api_version=None,
                           max_retries=10, timeout=60,
                           reuse_client=True, callback_manager=None, default_headers=None, http_client=None,
                           num_workers=cpu_count())

    index = VectorStoreIndex.from_documents(documents, embed_model=embed_model)

    return index

if __name__ == '__main__':
    config_path = 'db_config.yaml'
    db = MySQLDatabase(config_path)

    table_data = db.get_events()

    index = create_index_from_data(table_data)

    index.storage_context.persist()
