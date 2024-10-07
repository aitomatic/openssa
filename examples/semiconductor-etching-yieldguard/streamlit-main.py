from collections import defaultdict

from loguru import logger

import streamlit as st

from dana import get_or_create_dana


TITLE: str = 'Proactive _YieldGuard_ for Plasma Etchers'

st.set_page_config(page_title=TITLE,
                   page_icon=None,
                   layout='wide',
                   initial_sidebar_state='auto',
                   menu_items=None)

st.title(body=TITLE, anchor=None, help=None)

st.image('YieldGuard.png')


st.write('__PROBLEM__:')

if 'typed_problem' not in st.session_state:
    st.session_state.typed_problem: str = ''

st.session_state.typed_problem: str = st.text_area(label='Problem',
                                                   value=st.session_state.typed_problem,
                                                   height=3,
                                                   max_chars=None,
                                                   key=None,
                                                   help='Problem',
                                                   on_change=None, args=None, kwargs=None,
                                                   placeholder='Problem',
                                                   disabled=False,
                                                   label_visibility='collapsed')


if 'dana_solutions' not in st.session_state:
    st.session_state.dana_solutions: defaultdict[str, str] = defaultdict(str)

if st.button(label='SOLVE',
             on_click=None, args=None, kwargs=None,
             type='primary',
             disabled=False,
             use_container_width=False):
    with st.spinner(text='_SOLVING..._'):
        logger.level('DEBUG')

        st.session_state.dana_solutions[st.session_state.typed_problem]: str = \
            get_or_create_dana(use_semikong_lm=False).solve(problem=st.session_state.typed_problem)

if (solution := st.session_state.dana_solutions[st.session_state.typed_problem]):
    st.markdown(body=solution.replace('$', r'\$'))
