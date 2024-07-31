from llama_index.core import SummaryIndex
from llama_index.readers.web import SimpleWebPageReader

from llama_index.core import DocumentSummaryIndex
from llama_index.core import get_response_synthesizer
from llama_index.llms.openai import OpenAI
from llama_index.core.node_parser import SentenceSplitter


from openssa.l2.resource.abstract import AbstractResource
from openssa.l2.resource._global import global_register

from datetime import datetime
from dotenv import load_dotenv

load_dotenv()


@global_register
class WebPageResource(AbstractResource):
    """Webpage Informational Resource."""
    def __init__(self, url: str):
        self.url: str = url
        self.creation_time: datetime = datetime.now()
        self.document = None
        self.doc_summary_index = None
        print("webpage resource created")

    def unique_name(self) -> str:
        return f"{self.url}_{self.creation_time.isoformat(sep="_")}"

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
        # LLM (gpt-3.5-turbo)
        # TO-DOange to default LLM
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

    def answer(self, question: str, n_words: int = 1000) -> str:
        """Answer question from Informational Resource."""
        index = SummaryIndex.from_documents(self.get_document())
        # set Logging to DEBUG for more detailed outputs
        query_engine = index.as_query_engine()
        response = query_engine.query(question)
        return response


def test_example():
    test_url = "http://paulgraham.com/worked.html"
    test_url = "https://www.usa.gov/about-the-us"
    test_question = "What did the author do growing up?"

    webpage1 = WebPageResource(test_url)
    print(f"unique name = {webpage1.name()}")
    print(f"unique name = {webpage1.unique_name()}")
    print(f"answer = {webpage1.answer(test_question)}")
    print(f"summary = {webpage1.get_summary()}")


test_example()
