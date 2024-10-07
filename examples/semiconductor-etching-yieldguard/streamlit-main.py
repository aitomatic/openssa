from collections import defaultdict
from pathlib import Path

from pandas import read_csv
from loguru import logger
import streamlit as st

from dana import get_or_create_dana


TITLE: str = 'Proactive _YieldGuard_ for Plasma Etchers'

DATA_FILE_PATH: Path = 'measurements.csv'

MONITORING_PROBLEMS: dict[str, str] = {
    'RF Power Fluctuation': 'identify any RF power fluctuation issue from the data, and recommend what to do',
}


st.set_page_config(page_title=TITLE,
                   page_icon=None,
                   layout='wide',
                   initial_sidebar_state='auto',
                   menu_items=None)

st.title(body=TITLE, anchor=None, help=None)

st.image('YieldGuard.png')


st.dataframe(data=read_csv(DATA_FILE_PATH),
             width=None, height=None,
             use_container_width=False,
             hide_index=True,
             column_order=None,
             column_config=None,
             key=None,
             on_select='ignore',
             selection_mode='multi-row')


if 'dana_solutions' not in st.session_state:
    st.session_state.dana_solutions: defaultdict[str, str] = defaultdict(str)

for monitored_issue, problem in MONITORING_PROBLEMS.items():
    if st.button(label=f'ANALYZE: {monitored_issue}',
                 on_click=None, args=None, kwargs=None,
                 type='primary',
                 disabled=False,
                 use_container_width=False):
        with st.spinner(text='_ANALYZING..._'):
            logger.level('DEBUG')

            st.session_state.dana_solutions[monitored_issue]: str = \
                get_or_create_dana(use_semikong_lm=False).solve(problem=problem)

    if (solution := st.session_state.dana_solutions[monitored_issue]):
        st.markdown(body=solution.replace('$', r'\$'))
