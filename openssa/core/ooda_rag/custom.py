from llama_index import Document, Response, SimpleDirectoryReader, ServiceContext, OpenAIEmbedding
from llama_index.evaluation import DatasetGenerator
from llama_index.llms.base import LLM as RAGLLM
from llama_index.node_parser import SimpleNodeParser

from openssa.core.backend.abstract_backend import AbstractBackend
from openssa.core.slm.base_slm import PassthroughSLM
from openssa.core.ssm.rag_ssm import RAGSSM
from openssa.integrations.llama_index.backend import Backend as LlamaIndexBackend
from openssa.utils.llm_config import LLMConfig

FILE_NAME = "file_name"


class CustomBackend(LlamaIndexBackend):  # type: ignore
    def __init__(self, rag_llm: RAGLLM = None, service_context=None) -> None:  # type: ignore
        super().__init__(rag_llm=rag_llm, service_context=service_context)

    def _do_read_directory(self, storage_dir: str) -> None:
        def filename_fn(filename: str) -> dict:
            return {FILE_NAME: filename}

        documents = SimpleDirectoryReader(
            input_dir=self._get_source_dir(storage_dir),
            input_files=None,
            exclude=None,
            exclude_hidden=False,  # non-default
            errors='strict',  # non-default
            recursive=True,  # non-default
            encoding='utf-8',
            filename_as_id=True,
            required_exts=None,
            file_extractor=None,
            num_files_limit=None,
            file_metadata=filename_fn,
        ).load_data()
        self.documents = documents
        self._create_index(documents, storage_dir)

    def get_citation_type(self, filename: str) -> str:
        extension = filename.split(".")[-1]
        return extension.strip().lower() if extension else "unknown"

    def get_citations(self, response: Response, source_path: str = "") -> list[dict]:
        citations: list = []
        print("metadata", response.metadata)
        if not response.metadata:
            return citations
        for data in response.metadata.values():
            filename = (
                data.get(FILE_NAME, "").strip() or data.get("filename", "").strip()
            )

            if not filename:
                continue
            filename = filename.split("/")[-1]
            citation_type = self.get_citation_type(filename)
            pages = [data.get("page_label")] if data.get("page_label") else []
            if source_path and not source_path.endswith("/"):
                source_path = source_path + "/"
            source = source_path + filename if source_path else filename
            citation = {"type": citation_type, "pages": pages, "source": source}
            citations.append(citation)
        return citations

    def add_feedback(self, doc: Document) -> None:
        nodes = SimpleNodeParser.from_defaults().get_nodes_from_documents([doc])
        self._index.insert_nodes(nodes)
        self.query_engine = self._index.as_query_engine()

    def persist(self, persist_path: str) -> None:
        print("persist_path", persist_path)
        self._index.storage_context.persist(persist_path)

    def query(self, query: str, source_path: str = "") -> dict:  # pylint: disable=arguments-renamed
        """Returns a response dict with keys role, content, and citations."""
        if self.query_engine is None:
            return {"content": "No index to query. Please load something first."}
        response: Response = self.query_engine.query(query)
        citations = self.get_citations(response, source_path)
        print("citations", citations)
        return {"content": response.response, "citations": citations}

    async def get_evaluation_data(self) -> list:
        if self.documents:
            data_generator = DatasetGenerator.from_documents(self.documents)
            nodes = self.sort_longest_nodes(self.documents)
            service_context = LLMConfig.get_service_context_openai_35_turbo()
            data_generator = DatasetGenerator(
                nodes=nodes[:5],
                service_context=service_context,
                num_questions_per_chunk=3,
                show_progress=True,
            )
            eval_questions = await data_generator.agenerate_questions_from_nodes(5)
            return eval_questions
        return []

    def sort_longest_nodes(self, documents: list) -> list:
        return sorted(documents, key=lambda doc: len(doc.text), reverse=True)


class CustomSSM(RAGSSM):  # type: ignore
    def __init__(
        self,
        custom_rag_backend: AbstractBackend = None,
        s3_source_path: str = "",
        llm: RAGLLM = LLMConfig.get_aitomatic_yi_34b(),  # type: ignore
        embed_model: OpenAIEmbedding = LLMConfig.get_aito_embeddings()
    ) -> None:
        if custom_rag_backend is None:
            service_context = ServiceContext.from_defaults(llm=llm, embed_model=embed_model)
            custom_rag_backend = CustomBackend(rag_llm=llm, service_context=service_context)

        slm = PassthroughSLM()
        self._rag_backend = custom_rag_backend
        self.s3_source_path = s3_source_path
        super().__init__(slm=slm, rag_backend=self._rag_backend)

    def discuss(self, query: str, conversation_id: str = "") -> dict:  # pylint: disable=arguments-renamed
        """Return response with keys role, content, and citations."""
        return self._rag_backend.query(query, source_path=self.s3_source_path)

    def add_feedback(self, doc: Document, storage_path: str = "") -> None:
        self._rag_backend.add_feedback(doc)
        self._rag_backend.persist(storage_path)

    async def get_evaluation_data(self) -> dict:
        return await self._rag_backend.get_evaluation_data()
