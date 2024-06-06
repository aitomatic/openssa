# pylint: disable=bare-except,no-name-in-module,wrong-import-order,wrong-import-position


import streamlit as st
from pathlib import Path

from loguru import logger

from streamlit_extras.capture import logcapture

from data_and_knowledge import (
    DocName, FbId,
    DOC_LINKS_BY_NAME, DOC_NAMES_BY_FB_ID, FB_IDS_BY_DOC_NAME, QS_BY_FB_ID,
    EXPERT_PLAN_MAP, LOCAL_CACHE_DIR_PATH
)
from htp_oodar_agent import get_or_create_agent, expert_plan_from_fb_id
from llama_index.core import StorageContext, load_index_from_storage  # noqa: E402


DOC_NAMES: list[DocName] = sorted({DOC_NAMES_BY_FB_ID[fb_id] for fb_id in EXPERT_PLAN_MAP})
REPRESENTATIVE_FB_IDS_BY_DOC_NAME: dict[FbId, list[DocName]] = {doc_name: (set(FB_IDS_BY_DOC_NAME[doc_name])
                                                                           .intersection(EXPERT_PLAN_MAP))
                                                                for doc_name in DOC_NAMES}


TITLE: str = 'OpenSSA: Analysing SEC Filings with Planning & Reasoning'


def get_or_create_simple_rag_ssa(problem_id: str):  # noqa: E999, ANN201
    DATA_SRC_INDEX_DIR_PATH: Path = LOCAL_CACHE_DIR_PATH / 'docs' / DOC_NAMES_BY_FB_ID[problem_id] / '.text-embedding-ada-002'  # noqa: N806
    storage_context = StorageContext.from_defaults(persist_dir=DATA_SRC_INDEX_DIR_PATH)
    index = load_index_from_storage(storage_context)
    return index.as_query_engine()


def get_answer_simple(problem: str, problem_id: str) -> str:
    ssa = get_or_create_simple_rag_ssa(problem_id)
    solution = ssa.query(problem).response
    return solution


st.set_page_config(page_title=TITLE,
                   page_icon=None,
                   layout='wide',
                   initial_sidebar_state='auto',
                   menu_items=None)

st.title(body=TITLE, anchor=None, help=None)


if 'doc_name' not in st.session_state:
    st.session_state.doc_name: str = DOC_NAMES[0]

st.write('__SEC FILING__')
st.session_state.doc_name: str = st.selectbox(label='SEC Filing',
                                              options=DOC_NAMES,
                                              index=DOC_NAMES.index(st.session_state.doc_name),
                                              # format_func=None,
                                              key=None,
                                              help='SEC Filing',
                                              on_change=None, args=None, kwargs=None,
                                              placeholder='SEC Filing',
                                              disabled=False,
                                              label_visibility='collapsed')

st.write(DOC_LINKS_BY_NAME[st.session_state.doc_name])


st.write('__PROBLEM__')
problem_id: str = st.selectbox(label='Problem',
                               options=REPRESENTATIVE_FB_IDS_BY_DOC_NAME[st.session_state.doc_name],
                               index=0,
                               format_func=lambda i: QS_BY_FB_ID[i],
                               key=None,
                               help='Problem',
                               on_change=None, args=None, kwargs=None,
                               placeholder='Problem',
                               disabled=False,
                               label_visibility='collapsed')


# Initialize session state variables
if 'question_answered' not in st.session_state:
    st.session_state.question_answered = False
if 'current_answer' not in st.session_state:
    st.session_state.current_answer = ""
if 'all_answers' not in st.session_state:
    st.session_state.all_answers = []

if st.button(label='ANSWER WITH TYPICAL RAG'):
    with st.spinner(text='_SOLVING..._'):
        solution: str = get_answer_simple(problem=QS_BY_FB_ID[problem_id], problem_id=problem_id)
        st.session_state.current_answer = solution
        st.session_state.question_answered = True

if st.session_state.question_answered:
    st.write(st.session_state.current_answer)

if st.button(label='ANSWER WITH PLANNING AND REASONING',
             key=None,
             on_click=None, args=None, kwargs=None,
             type='primary',
             disabled=False,
             use_container_width=False):
    logger.level('DEBUG')
    with st.spinner(text='_THINKING..._'), logcapture(st.empty().code, from_logger=logger):
        solution: str = (get_or_create_agent(doc_name=st.session_state.doc_name, expert_knowledge=True)
                         .solve(problem=QS_BY_FB_ID[problem_id], plan=expert_plan_from_fb_id(problem_id), dynamic=False))

    if st.session_state.question_answered:
        st.session_state.all_answers.append(st.session_state.current_answer)
        st.session_state.question_answered = False
        st.session_state.current_answer = ""
    st.latex(body=solution)
