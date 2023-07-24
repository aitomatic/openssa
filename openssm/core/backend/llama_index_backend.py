from llama_index.indices.base import BaseIndex
from llama_index.indices.query.base import BaseQueryEngine
from llama_index import VectorStoreIndex, SimpleDirectoryReader, Response
from openssm.core.backend.base_backend import BaseBackend


class LlamaIndexBackend(BaseBackend):
    index: BaseIndex = None
    query_engine: BaseQueryEngine = None

    def __init__(self):
        super().__init__()

    # pylint: disable=unused-argument
    def query(self, conversation_id: str, user_input: list[dict]) -> list[dict]:
        if self.query_engine is None:
            response = "I'm sorry, I don't have an index to query. Please load something first."
        else:
            query = next((i['content'] for i in user_input if i['role'] == 'user'), None)
            response: Response = self.query_engine.query(query)
            response = response.response

        result = {"role": "assistant", "content": response}
        return [result]

    def read_directory(self, directory_path: str):
        documents = SimpleDirectoryReader(directory_path).load_data()
        self.index = VectorStoreIndex(documents)
        self.query_engine = self.index.as_query_engine()
