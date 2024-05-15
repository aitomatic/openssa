# pylint: disable=bare-except,no-name-in-module,wrong-import-position


import base64

import streamlit as st
from loguru import logger

from data_and_knowledge import DocName, FbId, Question, META_DF, EXPERT_PLAN_MAP
from htp_oodar_agent import solve_expert_htp_statically


IDS_FROM_EXPERT_PLAN_MAP = list(EXPERT_PLAN_MAP.keys())
FILTERED_META_DF = META_DF.loc[META_DF.index.isin(IDS_FROM_EXPERT_PLAN_MAP)]

FILTERERED_DOC_NAMES: list[DocName] = sorted(FILTERED_META_DF.doc_name.unique())
FILTERERED_DOC_LINKS_BY_NAME: dict[DocName, str] = dict(zip(FILTERED_META_DF.doc_name, FILTERED_META_DF.doc_link))
FILTERERED_DOC_NAMES_BY_FB_ID: dict[FbId, DocName] = FILTERED_META_DF.doc_name.to_dict()

FILTERERED_FB_IDS: list[FbId] = FILTERED_META_DF.index.unique().to_list()
FILTERERED_FB_IDS_BY_DOC_NAME: dict[FbId, list[DocName]] = FILTERED_META_DF.groupby('doc_name').apply(lambda _: _.index.to_list())
FILTERERED_QS_BY_FB_ID: dict[FbId, Question] = FILTERED_META_DF.question.to_dict()


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
                                            #   index=DOC_NAMES.index(st.session_state.doc_name), # noqa: E128
                                            #   format_func=None, # noqa: E128
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

# redirect_loguru_to_streamlit() #TODO: decide which logs should be shown

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
