from argparse import ArgumentParser
from functools import cache

from langchain import hub
from langchain.agents.agent import AgentExecutor
from langchain.agents.react.agent import create_react_agent
from langchain_community.tools.vectorstore.tool import VectorStoreQATool
from langchain_openai.llms.base import OpenAI

from data_and_knowledge import DocName, FbId, Answer, Doc, FB_ID_COL_NAME, DOC_NAMES_BY_FB_ID, QS_BY_FB_ID
from util import enable_batch_qa_and_eval, log_qa_and_update_output_file


prompt = hub.pull("hwchase17/react")
model = OpenAI()


@cache
def get_or_create_react_agent_executor(doc_name: DocName):
    tools = [
        ...
        # document path to encode: Doc(name=doc_name).dir_path
    ]

    return AgentExecutor(agent=create_react_agent(llm=model, tools=tools, prompt=prompt),
                         tools=tools)


@enable_batch_qa_and_eval(output_name='LangChain-ReAct')
@log_qa_and_update_output_file(output_name='LangChain-ReAct')
def solve(fb_id: FbId) -> Answer:
    return get_or_create_react_agent_executor(doc_name=DOC_NAMES_BY_FB_ID[fb_id]).invoke({'input': QS_BY_FB_ID[fb_id]})


if __name__ == '__main__':
    arg_parser = ArgumentParser()
    arg_parser.add_argument('fb_id')
    args = arg_parser.parse_args()

    solve(fb_id
          if (fb_id := args.fb_id).startswith(FB_ID_COL_NAME)
          else f'{FB_ID_COL_NAME}_{fb_id}')
