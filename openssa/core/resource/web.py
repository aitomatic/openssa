"""
=========================================
[future work] Web Informational Resources
=========================================
"""


from datetime import datetime, timezone

from googlesearch import search
from llama_index.core import DocumentSummaryIndex, SummaryIndex, get_response_synthesizer
from llama_index.core.node_parser import SentenceSplitter
from llama_index.llms.openai import OpenAI
from llama_index.readers.web import SimpleWebPageReader

from ._global import global_register
from .base import BaseResource


@global_register
class WebPageResource(BaseResource):
    """Webpage Informational Resource."""
    def __init__(self, url: str):
        self.url: str = url
        self.creation_time: datetime = datetime.now(timezone.utc)
        self.document = None
        self.doc_summary_index = None
        print("webpage resource created")

    @property
    def unique_name(self) -> str:
        return f"{self.url}_{self.creation_time.isoformat(sep="_")}"

    @property
    def name(self) -> str:
        return f"{self.url} created at {self.creation_time.isoformat(sep=" ")}"

    def make_document(self) -> None:
        self.document = SimpleWebPageReader(html_to_text=True).load_data([self.url])
        self.document[0].doc_id = "self"

    def get_document(self) -> SimpleWebPageReader:
        if self.document is None:
            self.make_document()
        return self.document

    def make_summary(self) -> None:
        llm = OpenAI(temperature=0, model="gpt-3.5-turbo")
        splitter = SentenceSplitter(chunk_size=1024)
        response_synthesizer = get_response_synthesizer(
            response_mode="tree_summarize", use_async=True
            )
        doc_summary_index = DocumentSummaryIndex.from_documents(
            self.get_document(),
            llm=llm,
            transformations=[splitter],
            response_synthesizer=response_synthesizer,
            show_progress=True,
            )
        self.doc_summary_index = doc_summary_index

    def get_summary(self) -> str:
        if self.doc_summary_index is None:
            self.make_summary()
        return self.doc_summary_index.get_document_summary("self")

    def answer(self, question: str, n_words: int = 1000) -> str:  # pylint: disable=unused-argument
        """Answer question from Informational Resource."""
        index = SummaryIndex.from_documents(self.get_document())
        # set Logging to DEBUG for more detailed outputs
        query_engine = index.as_query_engine()
        response = query_engine.query(question)
        return response


@global_register
class WebSearchResource(BaseResource):
    """Webpage Informational Resource."""
    def __init__(self, search_query: str):
        self.search_query: str = search_query
        self.creation_time: datetime = datetime.now(timezone.utc)
        print("web search resource created")

    @property
    def unique_name(self) -> str:
        return f"{"_".join(self.search_query.strip().split(" "))}_{self.creation_time.isoformat(sep="_")}"

    @property
    def name(self) -> str:
        return f"{self.search_query} created at {self.creation_time.isoformat(sep=" ")}"

    def fetch_top_search_results(self, query, num_results=10) -> list[str]:
        search_results = search(query, num_results=num_results)
        return list(search_results)

    def answer(self, question: str | None, n_words: int = 1000) -> str:  # pylint: disable=unused-argument
        """Answer question from Informational Resource."""
        urls = self.fetch_top_search_results(self.search_query)
        print(urls)
        urls = list(dict.fromkeys(urls))
        summary1 = WebPageResource(urls[0]).get_summary()
        summary2 = WebPageResource(urls[1]).get_summary()
        result = {
            "summary1": summary1,
            "summary2": summary2,
            "urls": urls[2:]
        }
        return result
