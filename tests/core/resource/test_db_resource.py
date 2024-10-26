from dotenv import load_dotenv
from openssa.core.resource.db import DbResource

load_dotenv()


# TODO: Fix hallucination
# Given Data: [(1, 'Laptop', 100000), (2, 'Smartphone', 60000), (3, 'Headphones', 8000), (4, 'Keyboard', 3000), (5, 'Mouse', 2000), (6, 'Monitor', 25000), (7, 'Tablet', 50000), (8, 'Smartwatch', 20000), (9, 'Camera', 45000), (10, 'Speaker', 15000)]
# Answer: The item that is the most expensive from the given data is the Camera.
# The Answer Should be: Laptop(100000).
# How to fix it? Make query by vanna or change the process in llama_index?

def test_db_resource():
    test_query = "SELECT * FROM items"
    test_question = "Which item is the most expensive from given data?"

    rdb1 = DbResource(query=test_query)
    # print(f"unique name = {rdb1.name}")
    # print(f"unique name = {rdb1.unique_name}")
    # print(f"answer = {rdb1.answer(test_question)}")
    # print(f"summary = {rdb1.get_summary()}")
    _ = rdb1.answer(test_question)
    # assert isinstance(answer, str)
    print(_)


test_db_resource()
