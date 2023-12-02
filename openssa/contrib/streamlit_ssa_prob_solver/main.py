"""SSAProbSolver instance."""


from pathlib import Path
import sys
sys.path.insert(1, str(Path(__file__).parent.parent.parent.parent))

# pylint: disable=wrong-import-position
import streamlit as st
from openssa.contrib import StreamlitSSAProbSolver


st.set_page_config(page_title='Problem-Solving SSA',
                   page_icon=None,
                   layout='wide',
                   initial_sidebar_state='auto',
                   menu_items=None)

StreamlitSSAProbSolver(unique_name='PROBLEM-SOLVING SSA',
                       domain='Atomic Layer Deposition (ALD) for Semiconductor',
                       prob='I want to estimate the ALD process time for: ...',
                       doc_src_path='s3://aitomatic-public/KnowledgeBase/Semiconductor')
