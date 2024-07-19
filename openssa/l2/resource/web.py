"""
=========================================
[future work] Web Informational Resources
=========================================
"""


from .abstract import AbstractResource
from ._global import global_register

from datetime import datetime


from llama_index.core import SummaryIndex
from llama_index.readers.web import SimpleWebPageReader

@global_register
class WebPageResource(AbstractResource):
    """Webpage Informational Resource."""
    def __init__(self, url: str):
        self.url: str = url
        self.creation_time: datetime = datetime.now()

    def unique_name(self) -> str:
        return f"{self.url}_{self.creation_time.isoformat(sep="_")}"

    def name(self) -> str:
        return f"{self.url} created at {self.creation_time.isoformat(sep=" ")}"

    def answer(self, question: str, n_words: int = 1000) -> str:
        """Answer question from Informational Resource."""
        documents = SimpleWebPageReader(html_to_text=True).load_data([self.url])
        index = SummaryIndex.from_documents(documents)
        # set Logging to DEBUG for more detailed outputs
        query_engine = index.as_query_engine()
        response = query_engine.query("What did the author do growing up?")
        return response

@global_register
class WebSearchResource(AbstractResource):
    """Web-Search Informational Resource."""
