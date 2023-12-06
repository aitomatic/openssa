# pylint: disable=invalid-name


"""Semiconductor ALD SSAProbSolver."""


import streamlit as st

from openssa.contrib import StreamlitSSAProbSolver


st.set_page_config(page_title='Problem-Solving SSA',
                   page_icon=None,
                   layout='wide',
                   initial_sidebar_state='auto',
                   menu_items=None)

StreamlitSSAProbSolver(unique_name='PROBLEM-SOLVING SSA',
                       domain='Atomic Layer Deposition (ALD) for Semiconductor',
                       problem=('Estimate the ALD process time for 10 cycles, '
                                'each with Pulse Time = 15 secs, Purge Time = 10 secs and negligible Inert'),
                       expert_heuristics=('Purge Time must be at least as long as Pulse Time in each cycle '
                                          'to ensure all excess precursor and reaction byproducts are removed '
                                          'from the chamber before the next cycle begins'),
                       doc_src_path='s3://aitomatic-public/KnowledgeBase/Semiconductor/ALD/ALD-Process.txt')
