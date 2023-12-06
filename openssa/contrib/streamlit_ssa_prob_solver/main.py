from pathlib import Path
import sys

import streamlit as st


sys.path.insert(1, str(Path(__file__).parent.parent.parent.parent))


st.set_page_config(page_title='Problem-Solving SSA',
                   page_icon=None,
                   layout='wide',
                   initial_sidebar_state='auto',
                   menu_items=None)
