from dotenv import load_dotenv
from openssa.core.resource.web import WebSearchResource

load_dotenv()


def test_websearch_resource():
    test_query = "united states of america"
    websearch1 = WebSearchResource(test_query)
    # print(f"unique name = {websearch1.name}")
    # print(f"unique name = {websearch1.unique_name}")
    # print(websearch1.answer(question=""))
    _ = websearch1.answer(question="")
    # assert isinstance(answer, str)
