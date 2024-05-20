# pylint: disable=bare-except,no-name-in-module,wrong-import-order,wrong-import-position


import base64
import streamlit as st

from data_and_knowledge import (DocName, FbId, Doc,
                                DOC_LINKS_BY_NAME, DOC_NAMES_BY_FB_ID, FB_IDS_BY_DOC_NAME, QS_BY_FB_ID,
                                EXPERT_PLAN_MAP)
from htp_oodar_agent import expert_plan_from_fb_id, solve_expert_htp_statically


DOC_NAMES: list[DocName] = sorted({DOC_NAMES_BY_FB_ID[fb_id] for fb_id in EXPERT_PLAN_MAP})
REPRESENTATIVE_FB_IDS_BY_DOC_NAME: dict[FbId, list[DocName]] = {doc_name: (set(FB_IDS_BY_DOC_NAME[doc_name])
                                                                           .intersection(EXPERT_PLAN_MAP))
                                                                for doc_name in DOC_NAMES}


def display_pdf(file_path):
    # Opening file from file path
    with open(file_path, 'rb') as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')

    # Embedding PDF in HTML
    pdf_display = F'<embed src="data:application/pdf;base64,{base64_pdf}" width="1024" height="1024" type="application/pdf">'

    # Displaying File
    st.markdown(pdf_display, unsafe_allow_html=True)


TITLE: str = 'Analysing SEC Filings (`FinanceBench` Dataset) with Planning & Reasoning'


st.set_page_config(page_title=TITLE,
                   page_icon=None,
                   layout='wide',
                   initial_sidebar_state='auto',
                   menu_items=None)


st.title(TITLE)


if 'doc_name' not in st.session_state:
    st.session_state.doc_name: str = DOC_NAMES[0]

st.session_state.doc_name: str = st.selectbox(label='SEC Document',
                                              options=DOC_NAMES,
                                              index=DOC_NAMES.index(st.session_state.doc_name),
                                              # format_func=None,
                                              key=None,
                                              help='SEC Document',
                                              on_change=None, args=None, kwargs=None,
                                              placeholder='SEC Document',
                                              disabled=False,
                                              label_visibility='visible')

st.write(DOC_LINKS_BY_NAME[st.session_state.doc_name])

try:
    display_pdf(Doc(st.session_state.doc_name).file_path)
except:  # noqa: E722
    st.write('_(document cannot be rendered)_')


question_id: str = st.selectbox(label='Question',
                                options=REPRESENTATIVE_FB_IDS_BY_DOC_NAME[st.session_state.doc_name],
                                index=0,
                                format_func=lambda i: QS_BY_FB_ID[i],
                                key=None,
                                help='Question',
                                on_change=None, args=None, kwargs=None,
                                placeholder='Question',
                                disabled=False,
                                label_visibility='visible')


if st.button(label=f'__SOLVE__: _{QS_BY_FB_ID[question_id]}_',
             key=None,
             on_click=None, args=None, kwargs=None,
             type='primary',
             disabled=False,
             use_container_width=False):
    st.text(expert_plan_from_fb_id(question_id).pformat)

    with st.spinner('Solving... Please wait'):
        solution: str = solve_expert_htp_statically(question_id)

    st.markdown(solution)
