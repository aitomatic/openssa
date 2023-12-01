"""SSAProbSolver instance."""


from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parent.parent.parent.parent))

# pylint: disable=wrong-import-position
import streamlit as st
from openssa.contrib import StreamlitSSAProbSolver


st.set_page_config(page_title='Problem-Solving SSA',
                   page_icon=None,
                   layout='wide',
                   initial_sidebar_state='collapsed',
                   menu_items=None)

StreamlitSSAProbSolver('Problem-Solving SSA',
                       doc_src_path='s3://aitomatic-public/KnowledgeBase/Semiconductor')
