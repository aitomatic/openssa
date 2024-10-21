from collections import defaultdict

from loguru import logger
import streamlit as st

from openssa import OpenAILM

# pylint: disable=wrong-import-order
from agent import get_or_create_agent


TITLE: str = 'OpenSSA: Maritime-Specific Agent'


st.set_page_config(page_title=TITLE,
                   page_icon=None,
                   layout='wide',
                   initial_sidebar_state='auto',
                   menu_items=None)

st.title(body=TITLE, anchor=None, help=None)


DEFAULT_PROBLEM: str = (
    'A vessel on my port side coming to a crossing situation in my radar. SOG is being used. What to do?'
)


st.write('__PROBLEM/QUESTION__:')

if 'typed_problem' not in st.session_state:
    st.session_state.typed_problem: str = DEFAULT_PROBLEM + "Show the answer in detail."

st.session_state.typed_problem: str = st.text_area(label='Problem/Question',
                                                   value=st.session_state.typed_problem,
                                                   height=3,
                                                   max_chars=None,
                                                   key=None,
                                                   help='Problem/Question',
                                                   on_change=None, args=None, kwargs=None,
                                                   placeholder='Problem/Question',
                                                   disabled=False,
                                                   label_visibility='collapsed')


if 'agent_solutions' not in st.session_state:
    st.session_state.agent_solutions: defaultdict[str, str] = defaultdict(str)


st.subheader('MARITIME-SPECIFIC AGENT')

if st.button(label='SOLVE',
             on_click=None, args=None, kwargs=None,
             type='primary',
             disabled=False,
             use_container_width=False):
    with st.spinner(text='_SOLVING..._'):
        logger.level('DEBUG')

        st.session_state.agent_solutions[st.session_state.typed_problem]: str = \
            get_or_create_agent().solve(problem=st.session_state.typed_problem)


if (solution := st.session_state.agent_solutions[st.session_state.typed_problem]):
    st.markdown(body=solution)
