from dotenv import load_dotenv
# from openssa import DANA, DbResource
from openssa.core.agent.dana import DANA  # , FileResource
from openssa.core.resource.db import DbResource

from myvanna import generate_sql_from_prompt

load_dotenv()


def get_or_create_agent(query) -> DANA:
    return DANA(
        resources=[DbResource(query=query)]
    )


def solve(question, query) -> str:
    agent = get_or_create_agent(query)
    try:
        return agent.solve(problem=question)
    except Exception as err:
        return f'ERROR: {err}'


if __name__ == '__main__':
    QUESTION = (
        "Can you list the products in order of sales volume from highest to lowest?"
    )

    query = generate_sql_from_prompt(QUESTION)
    print(query)
    answer = solve(QUESTION, query)

    print('--------------------------------')
    print(answer)
    print('--------------------------------')
    print(query)
    print('--------------------------------')
