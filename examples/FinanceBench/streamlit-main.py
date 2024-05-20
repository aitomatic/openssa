# pylint: disable=bare-except,no-name-in-module,wrong-import-order,wrong-import-position


import streamlit as st

from data_and_knowledge import (DocName, FbId,
                                DOC_LINKS_BY_NAME, DOC_NAMES_BY_FB_ID, FB_IDS_BY_DOC_NAME, QS_BY_FB_ID,
                                EXPERT_PLAN_MAP)
from htp_oodar_agent import get_or_create_agent, expert_plan_from_fb_id


DOC_NAMES: list[DocName] = sorted({DOC_NAMES_BY_FB_ID[fb_id] for fb_id in EXPERT_PLAN_MAP})
REPRESENTATIVE_FB_IDS_BY_DOC_NAME: dict[FbId, list[DocName]] = {doc_name: (set(FB_IDS_BY_DOC_NAME[doc_name])
                                                                           .intersection(EXPERT_PLAN_MAP))
                                                                for doc_name in DOC_NAMES}


TITLE: str = 'Analysing SEC Filings (`FinanceBench` Dataset) with Planning & Reasoning'


st.set_page_config(page_title=TITLE,
                   page_icon=None,
                   layout='wide',
                   initial_sidebar_state='auto',
                   menu_items=None)


st.title(TITLE)


if 'doc_name' not in st.session_state:
    st.session_state.doc_name: str = DOC_NAMES[0]

st.session_state.doc_name: str = st.selectbox(label='SEC Filing',
                                              options=DOC_NAMES,
                                              index=DOC_NAMES.index(st.session_state.doc_name),
                                              # format_func=None,
                                              key=None,
                                              help='SEC Filing',
                                              on_change=None, args=None, kwargs=None,
                                              placeholder='SEC Filing',
                                              disabled=False,
                                              label_visibility='visible')

st.write(DOC_LINKS_BY_NAME[st.session_state.doc_name])


problem_id: str = st.selectbox(label='Problem',
                               options=REPRESENTATIVE_FB_IDS_BY_DOC_NAME[st.session_state.doc_name],
                               index=0,
                               format_func=lambda i: QS_BY_FB_ID[i],
                               key=None,
                               help='Problem',
                               on_change=None, args=None, kwargs=None,
                               placeholder='Problem',
                               disabled=False,
                               label_visibility='visible')


if st.button(label=f'__SOLVE__: _{QS_BY_FB_ID[problem_id]}_',
             key=None,
             on_click=None, args=None, kwargs=None,
             type='primary',
             disabled=False,
             use_container_width=False):
    st.text(expert_plan_from_fb_id(problem_id).pformat)

    with st.spinner('Solving...'):
        solution: str = (get_or_create_agent(doc_name=st.session_state.doc_name, expert_knowledge=True)
                         .solve(problem=QS_BY_FB_ID[problem_id], plan=expert_plan_from_fb_id(problem_id), dynamic=False))

    st.markdown(solution)
