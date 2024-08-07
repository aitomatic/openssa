from collections import defaultdict

from loguru import logger
import streamlit as st

from agent import get_or_create_agent


TITLE: str = 'OpenSSA: Semiconductor Industry-Specific Agent leveraging SemiKong LM'


st.set_page_config(page_title=TITLE,
                   page_icon=None,
                   layout='wide',
                   initial_sidebar_state='auto',
                   menu_items=None)

st.title(body=TITLE, anchor=None, help=None)


DEFAULT_PROBLEM: str = (
    'How to etch 2 um silicon dioxide (PR mask) using ICP RIE Plasmalab System 100... Any suggestions for recipe?'
    '\n'
    'I am trying to etch 2 μm of PECVD SiO2 using a ~4 μm PR mask to create a pattern of 20 * 60 μm. '
    'I am using the Oxford ICP-RIE Plasmalab System 100. '
    'I have tried multiple recipes, but I have encountered issues '
    'such as low selectivity, polymer redeposition, and extremely low etch rates at times.'
)


st.write('__PROBLEM/QUESTION__:')

if 'typed_problem' not in st.session_state:
    st.session_state.typed_problem: str = DEFAULT_PROBLEM

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


generic_agent, semikong_agent = st.columns(spec=2, gap='large')


if 'generic_agent_solutions' not in st.session_state:
    st.session_state.generic_agent_solutions: defaultdict[str, str] = defaultdict(str)


with generic_agent:
    st.subheader('Generic Agent')
    st.subheader('_using generic LM_')

    if st.button(label='SOLVE',
                 on_click=None, args=None, kwargs=None,
                 type='secondary',
                 disabled=False,
                 use_container_width=False):
        with st.spinner(text='_SOLVING..._'):
            logger.level('DEBUG')

            st.session_state.generic_agent_solutions[st.session_state.typed_problem]: str = \
                get_or_create_agent(use_semikong_lm=False).solve(problem=st.session_state.typed_problem)

    if (solution := st.session_state.generic_agent_solutions[st.session_state.typed_problem]):
        st.markdown(body=solution.replace('$', r'\$'))


if 'semikong_agent_solutions' not in st.session_state:
    st.session_state.semikong_agent_solutions: defaultdict[str, str] = defaultdict(str)


with semikong_agent:
    st.subheader('SEMICONDUCTOR INDUSTRY AGENT')
    st.subheader('_using `SemiKong` LM_')

    if st.button(label='SOLVE',
                 on_click=None, args=None, kwargs=None,
                 type='primary',
                 disabled=False,
                 use_container_width=False):
        with st.spinner(text='_SOLVING..._'):
            logger.level('DEBUG')

            st.session_state.semikong_agent_solutions[st.session_state.typed_problem]: str = \
                get_or_create_agent(use_semikong_lm=True).solve(problem=st.session_state.typed_problem)

    if (solution := st.session_state.semikong_agent_solutions[st.session_state.typed_problem]):
        st.markdown(body=solution.replace('$', r'\$'))
