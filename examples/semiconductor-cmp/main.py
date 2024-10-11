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
    'Explore Smoothing Process': 'I am trying to smoothen a silicon surface that is 1.5-2.5 microns in depth. I have tried a hot concentrated KOH solution, but it results in a thickness of 8-9 microns. Give me a list of potential solutions along with the pros and cons of each approach.',
    'Recipe for CMP': 'Recommend a detailed recipe for the Chemical Mechanical Polishing approach that you have listed above.',
    'Post-cleaning for under-50 nm Geometries': 'For advanced geometries below 50nm, can you recommend additional post-CMP cleaning?',
}

problem = "I am trying to smoothen a silicon surface that is 1.5-2.5 microns in depth. I have tried a hot concentrated KOH solution, but it results in a thickness of 8-9 microns. Give me a list of potential solutions along with the pros and cons of each approach."
print(get_or_create_dana(use_semikong_lm=False).solve(problem=problem))

# st.set_page_config(page_title=TITLE,
#                    page_icon=None,
#                    layout='wide',
#                    initial_sidebar_state='auto',
#                    menu_items=None)

# st.title(body=TITLE, anchor=None, help=None)

# st.image(str(CWD_PATH / 'cmp-machine.png'))


# st.dataframe(data=read_csv(DATA_FILE_PATH),
#              width=None, height=None,
#              use_container_width=False,
#              hide_index=True,
#              column_order=None,
#              column_config=None,
#              key=None,
#              on_select='ignore',
#              selection_mode='multi-row')


# if 'dana_analyses' not in st.session_state:
#     st.session_state.dana_analyses: defaultdict[str, str] = defaultdict(str)

# for monitored_issue, problem in MONITORING_PROBLEMS.items():
#     if st.button(label=f'_monitor_: {monitored_issue}',
#                  on_click=None, args=None, kwargs=None,
#                  type='primary',
#                  disabled=False,
#                  use_container_width=False):
#         with st.spinner(text='_analyzing..._'):
#             logger.level('DEBUG')

#             st.session_state.dana_analyses[monitored_issue]: str = \
#                 get_or_create_dana(use_semikong_lm=False).solve(problem=problem)

#     if (solution := st.session_state.dana_analyses[monitored_issue]):
#         st.markdown(body=solution.replace('$', r'\$'))
