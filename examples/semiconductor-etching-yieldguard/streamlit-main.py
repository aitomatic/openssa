from collections import defaultdict
from pathlib import Path

from pandas import read_csv
from loguru import logger
import streamlit as st

from dana import get_or_create_dana


TITLE: str = 'Proactive _YieldGuard_ for Plasma Etchers'

CWD_PATH: Path = Path(__file__).parent

DATA_FILE_PATH: Path = CWD_PATH / 'measurements.csv'

MONITORING_PROBLEMS: dict[str, str] = {
    'RF Power Fluctuation': 'identify any RF power fluctuation issue from the data, and recommend what to do',
    'Pressure Instability': 'identify any Pressure Instability issue from the data, and recommend what to do',
    'Chamber Wall Temperature': 'analyze Chamber Wall Temperature data and identify any cleaning needs',
}


st.set_page_config(page_title=TITLE,
                   page_icon=None,
                   layout='wide',
                   initial_sidebar_state='auto',
                   menu_items=None)

st.title(body=TITLE, anchor=None, help=None)

st.image(str(CWD_PATH / 'YieldGuard.png'))


st.dataframe(data=read_csv(DATA_FILE_PATH),
             width=None, height=None,
             use_container_width=False,
             hide_index=True,
             column_order=None,
             column_config=None,
             key=None,
             on_select='ignore',
             selection_mode='multi-row')


if 'dana_analyses' not in st.session_state:
    st.session_state.dana_analyses: defaultdict[str, str] = defaultdict(str)

for monitored_issue, problem in MONITORING_PROBLEMS.items():
    if st.button(label=f'_monitor_: {monitored_issue}',
                 on_click=None, args=None, kwargs=None,
                 type='primary',
                 disabled=False,
                 use_container_width=False):
        with st.spinner(text='_analyzing..._'):
            logger.level('DEBUG')

            st.session_state.dana_analyses[monitored_issue]: str = \
                get_or_create_dana(use_semikong_lm=False).solve(problem=problem)

    if (solution := st.session_state.dana_analyses[monitored_issue]):
        st.markdown(body=solution.replace('$', r'\$'))
