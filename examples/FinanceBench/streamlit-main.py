# pylint: disable=bare-except,no-name-in-module,wrong-import-position


import base64

import streamlit as st
from loguru import logger

from data_and_knowledge import FILTERERED_DOC_NAMES, FILTERERED_DOC_LINKS_BY_NAME, FILTERERED_QS_BY_FB_ID, FILTERERED_FB_IDS_BY_DOC_NAME
# , cache_file_path
from htp_oodar_agent import solve_expert_htp_statically


def display_pdf(file_path):
    # Opening file from file path
    with open(file_path, 'rb') as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')

    # Embedding PDF in HTML
    pdf_display = F'<embed src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf">'

    # Displaying File
    st.markdown(pdf_display, unsafe_allow_html=True)

def redirect_loguru_to_streamlit():
    def _filter_warning(record):
        return record["level"].no == logger.level("WARNING").no
    if 'warning_logger' not in st.session_state:
        st.session_state['warning_logger'] = logger.add(st.warning, filter=_filter_warning, level='INFO')
    if 'error_logger' not in st.session_state:
        st.session_state['error_logger'] = logger.add(st.error, level='ERROR')


st.set_page_config(page_title='Analyses of SEC Filings (`FinanceBench` Dataset)',
                   page_icon=None,
                   layout='centered',
                   initial_sidebar_state='auto',
                   menu_items=None)


st.title('Analyses of SEC Filings (`FinanceBench` Dataset)')


if 'doc_name' not in st.session_state:
    st.session_state.doc_name: str = FILTERERED_DOC_NAMES[0]

st.session_state.doc_name: str = st.selectbox(label='SEC Document',
                                              options=FILTERERED_DOC_NAMES,
                                            #   index=DOC_NAMES.index(st.session_state.doc_name),
                                              # format_func=None,
                                              key=None,
                                              help='SEC Document',
                                              on_change=None, args=None, kwargs=None,
                                              placeholder='SEC Document',
                                              disabled=False,
                                              label_visibility='hidden')

st.write(FILTERERED_DOC_LINKS_BY_NAME[st.session_state.doc_name])

# try:
#     display_pdf(cache_file_path(st.session_state.doc_name))
# except:  # noqa: E722
#     print('document cannot be rendered')


question_id: str = st.selectbox(label='Question',
                                # options=FILTERERED_DOC_NAMES[st.session_state.doc_name],
                                options=FILTERERED_FB_IDS_BY_DOC_NAME[st.session_state.doc_name],
                                index=0,
                                format_func=lambda i: FILTERERED_QS_BY_FB_ID[i],
                                key=None,
                                help='Question',
                                on_change=None, args=None, kwargs=None,
                                placeholder='Question',
                                disabled=False,
                                label_visibility='visible')

# redirect_loguru_to_streamlit() #TODO decide which logs should be shown

if st.button(label=f'__SOLVE__: _{FILTERERED_QS_BY_FB_ID[question_id]}_',
             key=None,
             on_click=None, args=None, kwargs=None,
             type='primary',
             disabled=False,
             use_container_width=False):
    with st.spinner('Solving... Please wait'):
        solution: str = solve_expert_htp_statically(question_id)
    st.write(solution)
    # st.text(solution)
