from llama_index.llms.azure_openai import AzureOpenAI
from llama_index.embeddings.azure_openai import AzureOpenAIEmbedding as LlamaEmbedding
from llama_index.core import Settings
from .config import LMConfig

azure_llama_index_lm = AzureOpenAI(
    deployment_name=LMConfig.AZURE_OPENAI_GPT_DEPLOYMENT_NAME,
    api_key=LMConfig.AZURE_OPENAI_API_KEY,
    azure_endpoint=LMConfig.AZURE_OPENAI_ENDPOINT,
    api_version=LMConfig.AZURE_OPENAI_API_VERSION,
)

azure_llama_index_embedding = LlamaEmbedding(
    deployment_name=LMConfig.AZURE_OPENAI_EMBEDDING_DEPLOYMENT_NAME,
    api_key=LMConfig.AZURE_OPENAI_API_KEY,
    azure_endpoint=LMConfig.AZURE_OPENAI_ENDPOINT,
    api_version=LMConfig.AZURE_OPENAI_API_VERSION
)

Settings.llm = azure_llama_index_lm
Settings.embed_model = azure_llama_index_embedding
