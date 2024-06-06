# pylint: disable=bare-except,no-name-in-module,wrong-import-order,wrong-import-position


from loguru import logger
import streamlit as st
from streamlit_extras.capture import logcapture

from data_and_knowledge import (DocName, FbId,
                                DOC_LINKS_BY_NAME, DOC_NAMES_BY_FB_ID, FB_IDS_BY_DOC_NAME, QS_BY_FB_ID,
                                EXPERT_PLAN_MAP)
from htp_oodar_agent import get_or_create_agent, expert_plan_from_fb_id
from rag_default import get_or_create_file_resource


DOC_NAMES: list[DocName] = sorted({DOC_NAMES_BY_FB_ID[fb_id] for fb_id in EXPERT_PLAN_MAP}
                                  .difference(('BOEING_2022_10K',
                                               'AES_2022_10K', 'MGMRESORTS_2018_10K', 'NETFLIX_2017_10K')))
REPRESENTATIVE_FB_IDS_BY_DOC_NAME: dict[FbId, list[DocName]] = {doc_name: (set(FB_IDS_BY_DOC_NAME[doc_name])
                                                                           .intersection(EXPERT_PLAN_MAP))
                                                                for doc_name in DOC_NAMES}


TITLE: str = 'OpenSSA: Analysing SEC Filings with Planning & Reasoning'

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


if 'question_answered' not in st.session_state:
    st.session_state.question_answered: bool = False

if 'current_answer' not in st.session_state:
    st.session_state.current_answer: str = ''


if st.button(label=f'__ANSWER WITH 1-PASS RAG__: _{QS_BY_FB_ID[problem_id]}_',
             # key=None,
             on_click=None, args=None, kwargs=None,
             type='secondary',
             disabled=False,
             use_container_width=False):
    with st.spinner(text='_ATTEMPTING TO RETRIEVE ANSWER..._'):
        solution: str = get_or_create_file_resource(doc_name=st.session_state.doc_name).answer(question=QS_BY_FB_ID[problem_id])
        st.session_state.current_answer: str = solution
        st.session_state.question_answered: bool = True

if st.session_state.question_answered:
    st.markdown(body=st.session_state.current_answer)


if st.button(label=f'__SOLVE WITH PLANNING & REASONING__: _{QS_BY_FB_ID[problem_id]}_',
             # key=None,
             on_click=None, args=None, kwargs=None,
             type='primary',
             disabled=False,
             use_container_width=False):
    logger.level('DEBUG')
    with st.spinner(text='_THINKING..._'), logcapture(st.empty().code, from_logger=logger):
        solution: str = (get_or_create_agent(doc_name=st.session_state.doc_name, expert_knowledge=True)
                         .solve(problem=QS_BY_FB_ID[problem_id], plan=expert_plan_from_fb_id(problem_id), dynamic=False))

    if st.session_state.question_answered:
        st.session_state.question_answered: bool = False
        st.session_state.current_answer: str = ''

    st.markdown(body=solution.replace('$', r'\$'))
