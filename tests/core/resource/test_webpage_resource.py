from dotenv import load_dotenv
from openssa.core.resource.web import WebPageResource

load_dotenv()


def test_webpage_resource():
    test_url = "http://paulgraham.com/worked.html"
    test_question = "What did the author do growing up?"

    webpage1 = WebPageResource(test_url)
    # print(f"unique name = {webpage1.name}")
    # print(f"unique name = {webpage1.unique_name}")
    # print(f"answer = {webpage1.answer(test_question)}")
    # print(f"summary = {webpage1.get_summary()}")
    _ = webpage1.answer(test_question)
    _ = webpage1.get_summary()
    # assert isinstance(answer, str)
    # assert isinstance(summary, str)
