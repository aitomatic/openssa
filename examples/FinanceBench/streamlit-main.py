from collections import defaultdict
from functools import cache

from loguru import logger
import streamlit as st

from data_and_knowledge import DocName, Doc, DOC_NAMES, ExpertPlanId as TaskId, EXPERT_PROGRAMS
from dana import get_or_create_agent, get_or_create_adaptations
from rag import get_or_create_file_resource


TASK_IDS: list[TaskId] = list(EXPERT_PROGRAMS)
TASK_IDS.insert(0, '')

DOC_NAMES: list[DocName] = sorted(set(DOC_NAMES)
                                  .difference(('BOEING_2022_10K',
                                               'AES_2022_10K', 'MGMRESORTS_2018_10K', 'NETFLIX_2017_10K')))


TITLE: str = 'OpenSSA: Analyzing SEC Filings with Domain-Aware Neurosymbolic Agent (DANA)'

st.set_page_config(page_title=TITLE,
                   page_icon=None,
                   layout='wide',
                   initial_sidebar_state='auto',
                   menu_items=None)

st.title(body=TITLE, anchor=None, help=None)


if 'task_id' not in st.session_state:
    st.session_state.task_id: str = TASK_IDS[0]


if 'typed_question' not in st.session_state:
    st.session_state.typed_question: str = "What is the company's Total Revenue in its latest fiscal period?"


@cache
def task_statement_template(task_id: TaskId, /) -> str:
    return EXPERT_PROGRAMS[task_id]['task']


@cache
def task_statement(task_id: TaskId, doc_name: DocName) -> str:
    return (task_statement_template(task_id).format(COMPANY=(doc := Doc(name=doc_name)).company, PERIOD=doc.period)
            if task_id
            else st.session_state.typed_question)


st.write('__QUESTION/TASK__:')
st.session_state.task_id: str = st.selectbox(label='Task',
                                             options=TASK_IDS,
                                             index=TASK_IDS.index(st.session_state.task_id),
                                             format_func=lambda i: (task_statement_template(i).split('\n')[0]
                                                                    if i
                                                                    else '<TYPE QUESTION IN BELOW BOX>'),
                                             key=None,
                                             help='Task',
                                             on_change=None, args=None, kwargs=None,
                                             placeholder='Task',
                                             disabled=False,
                                             label_visibility='collapsed')


if not st.session_state.task_id:
    st.session_state.typed_question: str = st.text_area(label='Question',
                                                        value=st.session_state.typed_question,
                                                        height=68,
                                                        max_chars=None,
                                                        key=None,
                                                        help='Type a Question',
                                                        on_change=None, args=None, kwargs=None,
                                                        placeholder='Type a Question',
                                                        disabled=False,
                                                        label_visibility='collapsed')


if 'doc_name' not in st.session_state:
    st.session_state.doc_name: str = 'AMD_2022_10K'

st.write('based on __SEC FILING__:')
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


task_doc_pair: tuple[TaskId, DocName] = (st.session_state.task_id or st.session_state.typed_question,
                                         st.session_state.doc_name)


question: str = task_statement(task_id=st.session_state.task_id, doc_name=st.session_state.doc_name)


rag, pr = st.columns(spec=2, gap='large')


if 'rag_answers' not in st.session_state:
    st.session_state.rag_answers: defaultdict[tuple[TaskId, DocName], str] = defaultdict(str)


with rag:
    st.subheader('Retrieval-Augmented Generation (RAG)')
    st.subheader('_with standard settings_')

    if st.button(label='Answer',
                 on_click=None, args=None, kwargs=None,
                 type='secondary',
                 disabled=False,
                 use_container_width=False):
        with st.spinner(text='_RETRIEVING INFO..._'):
            st.session_state.rag_answers[task_doc_pair]: str = (
                get_or_create_file_resource(doc_name=st.session_state.doc_name)
                .answer(question=question)
            )

    if (answer := st.session_state.rag_answers[task_doc_pair]):
        st.markdown(body=answer.replace('$', r'\$'))


if 'agent_solutions' not in st.session_state:
    st.session_state.agent_solutions: defaultdict[tuple[TaskId, DocName], str] = defaultdict(str)


with pr:
    st.subheader('FINANCIAL ANALYST AGENT')
    st.subheader('_with `OpenSSA` Planning & Reasoning_')

    if st.button(label='SOLVE',
                 on_click=None, args=None, kwargs=None,
                 type='primary',
                 disabled=False,
                 use_container_width=False):
        with st.spinner(text='_SOLVING..._'):
            logger.level('DEBUG')

            agent = get_or_create_agent(doc_name=st.session_state.doc_name,
                                        expert_knowledge=True, expert_programs=True,
                                        max_depth=3, max_subtasks_per_decomp=6,
                                        llama_index_openai_lm_name='gpt-4o-mini')

            st.session_state.agent_solutions[task_doc_pair]: str = (
                agent.solve(problem=question,
                            adaptations_from_known_programs=get_or_create_adaptations(doc_name=st.session_state.doc_name))
            )

    if (solution := st.session_state.agent_solutions[task_doc_pair]):
        st.markdown(body=solution.replace('$', r'\$'))
