from llama_index.core import SummaryIndex
from llama_index.readers.web import SimpleWebPageReader

from googlesearch import search

from openssa.l2.resource.abstract import AbstractResource
from openssa.l2.resource._global import global_register
from openssa.l2.resource.webpage_test import WebPageResource

from datetime import datetime
from dotenv import load_dotenv

load_dotenv()


@global_register
class WebSearchResource(AbstractResource):
    """Webpage Informational Resource."""
    def __init__(self, search_query: str):
        self.search_query: str = search_query
        self.creation_time: datetime = datetime.now()
        print("web search resource created")

    def unique_name(self) -> str:
        return f"{"_".join(self.search_query.strip().split(" "))}_{self.creation_time.isoformat(sep="_")}"

    def name(self) -> str:
        return f"{self.search_query} created at {self.creation_time.isoformat(sep=" ")}"

    def fetch_top_search_results(self, query, num_results=10) -> list[str]:
        search_results = search(query, num_results=num_results)
        # print(type(search_results))
        # for x in search_results:
        #     print(type(x), x)
        # return [str(url) for url in search_results]
        return list(search_results)

    def answer(self, question: str | None, n_words: int = 1000) -> str:
        """Answer question from Informational Resource."""
        urls = self.fetch_top_search_results(self.search_query)
        print(urls)
        urls = list(dict.fromkeys(urls))
        # webpage1 = WebPageResource(urls[0])
        # webpage2 = WebPageResource(urls[1])
        summary1 = WebPageResource(urls[0]).get_summary()
        summary2 = WebPageResource(urls[1]).get_summary()
        result = {
            "summary1": summary1,
            "summary2": summary2,
            "urls": urls[2:]
        }
        return result

def test_example():
    test_query = "united states of america"
    websearch1 = WebSearchResource(test_query)
    print(f"unique name = {websearch1.name()}")
    print(f"unique name = {websearch1.unique_name()}")
    print(websearch1.answer(question=""))


test_example()
