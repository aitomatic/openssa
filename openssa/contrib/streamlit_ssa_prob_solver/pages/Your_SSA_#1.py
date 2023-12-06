# pylint: disable=invalid-name


"""SSAProbSolver instance #1."""


import streamlit as st

from openssa.contrib import StreamlitSSAProbSolver


st.set_page_config(page_title='Problem-Solving SSA',
                   page_icon=None,
                   layout='wide',
                   initial_sidebar_state='auto',
                   menu_items=None)

StreamlitSSAProbSolver(unique_name='SSA #1')
