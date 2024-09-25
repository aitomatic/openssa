from __future__ import annotations

from argparse import ArgumentParser
from functools import cache
from typing import TYPE_CHECKING

from langchain import hub
from langchain.agents.agent import AgentExecutor
from langchain.agents.react.agent import create_react_agent
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.tools.vectorstore.tool import VectorStoreQATool
from langchain_community.vectorstores.faiss import FAISS
from langchain_openai.embeddings.base import OpenAIEmbeddings
from langchain_openai.chat_models.base import ChatOpenAI
from langchain_text_splitters.character import RecursiveCharacterTextSplitter

from data_and_knowledge import DocName, FbId, Answer, Doc, FB_ID_COL_NAME, DOC_NAMES_BY_FB_ID, QS_BY_FB_ID
from util import enable_batch_qa_and_eval, log_qa_and_update_output_file

from openssa.core.util.lm.config import LMConfig

if TYPE_CHECKING:
    from langchain_core.documents.base import Document
    from langchain_core.embeddings.embeddings import Embeddings
    from langchain_core.language_models.llms import BaseLLM
    from langchain_core.tools import BaseTool
    from langchain_core.vectorstores.base import VectorStore


EMBED_MODEL: Embeddings = OpenAIEmbeddings(model='text-embedding-3-large', dimensions=3072, chunk_size=2048)
LLM: BaseLLM = ChatOpenAI(model_name='gpt-4o', temperature=0, seed=LMConfig.DEFAULT_SEED, n=1, max_tokens=2048)

REACT_PROMPT_TEMPLATE: str = hub.pull('hwchase17/react')


@cache
def get_or_create_react_agent_executor(doc_name: DocName):
    doc: Doc = Doc(name=doc_name)

    tools: list[BaseTool] = [
        VectorStoreQATool(
            name=doc_name,
            description=f'{doc.type} SEC Filing by {doc.company} for financial period {doc.period}',
            vectorstore=FAISS.from_documents(
                documents=(PyPDFLoader(file_path=doc.file_path)
                           .load_and_split(text_splitter=RecursiveCharacterTextSplitter())),
                embedding=EMBED_MODEL),
            llm=LLM)
    ]

    return AgentExecutor(agent=create_react_agent(llm=LLM, tools=tools, prompt=REACT_PROMPT_TEMPLATE),
                         tools=tools,
                         return_intermediate_steps=True,
                         max_iterations=15,
                         max_execution_time=None,
                         early_stopping_method='force',  # TODO: 'generate'
                         handle_parsing_errors=True,
                         trim_intermediate_steps=-1)


@enable_batch_qa_and_eval(output_name='LangChain-ReAct')
@log_qa_and_update_output_file(output_name='LangChain-ReAct')
def solve(fb_id: FbId) -> Answer:
    return (get_or_create_react_agent_executor(doc_name=DOC_NAMES_BY_FB_ID[fb_id])
            .invoke({'input': QS_BY_FB_ID[fb_id]})['output'])


if __name__ == '__main__':
    arg_parser = ArgumentParser()
    arg_parser.add_argument('fb_id')
    arg_parser.add_argument('--from-id', action='store_true')
    args = arg_parser.parse_args()

    if not (fb_id := args.fb_id).startswith(FB_ID_COL_NAME):
        fb_id: FbId = f'{FB_ID_COL_NAME}_{fb_id}'

    solve(f'from:{fb_id}' if args.from_id else fb_id)
