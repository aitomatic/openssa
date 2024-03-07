# pylint: disable=bare-except,invalid-name,no-name-in-module,wrong-import-position


import base64
from pathlib import Path
import sys

import nest_asyncio
import streamlit as st

sys.path.insert(1, str(Path(__file__).parent.parent.parent))  # to use OpenSSA in same repo

from fb_ssa.data import DOC_LINKS_BY_NAME, QS_BY_ID, QAIDS_BY_DOC_NAME, cached_file_path  # noqa: E402
from fb_ssa.prob_solve import solve  # noqa: E402


DOC_NAMES: list[str] = [
    'ACTIVISIONBLIZZARD_2019_10K',
    'AMCOR_2023_10K',
    'AMD_2015_10K', 'AMD_2022_10K',
    'BESTBUY_2017_10K', 'BESTBUY_2023_10K',
    'BLOCK_2016_10K'
    'BOEING_2022_10K',
    'COCACOLA_2021_10K',
    'CORNING_2021_10K',
    'CVSHEALTH_2018_10K',
    'GENERALMILLS_2022_10K',
    'LOCKHEEDMARTIN_2022_10K',
    'MGMRESORTS_2020_10K',
    'NIKE_2018_10K', 'NIKE_2021_10K',
    'PAYPAL_2022_10K',
    'PEPSICO_2023_8K_dated-2023-05-30',
    'PFIZER_2021_10K',
    'VERIZON_2022_10K',
    'WALMART_2020_10K',
]


nest_asyncio.apply()


def display_pdf(file_path):
    # Opening file from file path
    with open(file_path, 'rb') as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')

    # Embedding PDF in HTML
    pdf_display = F'<embed src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf">'

    # Displaying File
    st.markdown(pdf_display, unsafe_allow_html=True)


st.set_page_config(page_title='Analyses of SEC Filings (`FinanceBench` Dataset) with aiVA',
                   page_icon=None,
                   layout='centered',
                   initial_sidebar_state='auto',
                   menu_items=None)


st.title('Analyses of SEC Filings (`FinanceBench` Dataset) with aiVA')


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
                                              label_visibility='hidden')

st.write(DOC_LINKS_BY_NAME[st.session_state.doc_name])

try:
    display_pdf(cached_file_path(st.session_state.doc_name))
except:  # noqa: E722
    print('document cannot be rendered')


question_id: str = st.selectbox(label='Question',
                                options=QAIDS_BY_DOC_NAME[st.session_state.doc_name],
                                index=0,
                                format_func=lambda i: QS_BY_ID[i],
                                key=None,
                                help='Question',
                                on_change=None, args=None, kwargs=None,
                                placeholder='Question',
                                disabled=False,
                                label_visibility='visible')

if st.button(label=f'__SOLVE__: _{QS_BY_ID[question_id]}_',
             key=None,
             on_click=None, args=None, kwargs=None,
             type='primary',
             disabled=False,
             use_container_width=False):
    solution: str = solve(question_id)
    st.write(solution)
    # st.text(solution)
