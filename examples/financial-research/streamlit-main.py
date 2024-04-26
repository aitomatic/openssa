# pylint: disable=bare-except,no-name-in-module,wrong-import-position


from pathlib import Path
import sys

from mechanize import Browser
import nest_asyncio
from pyhtml2pdf import converter
import streamlit as st

sys.path.insert(1, str(Path(__file__).parent.parent.parent))  # to use OpenSSA in same repo

from dataproc import get_or_create_cached_dir_path  # noqa: E402
from prob_solve import solve  # noqa: E402


DEFAULT_OBJECTIVE: str = (
    'I want to allocate some capital to higher-risk investments in high-growth computing hardware companies.\n\n'

    'I want companies with:\n'
    '- at least 30% growth in year-to-date revenue compared to last fiscal year,\n'
    '- at least 50% gross margin,\n'
    '- at most 40x Price-over-forward-Earnings ratio,\n'
    '- products used in AI-related computing.\n\n'

    "I DON'T want companies with 1-2 top customers, combined, making up more than 25% of revenue.\n\n"

    'Evaluate whether the following is a good fit for me: '
)


COMPANIES: str = [
    'Arista Networks (ANET)',
    'ARM Holdings (ARM)',
    'Super Micro Computer, Inc. (SMCI)',
    'Uber (UBER)',
]


nest_asyncio.apply()


st.set_page_config(page_title='Automated Financial Research by AI with Planning & Reasoning',
                   page_icon=None,
                   layout='centered',
                   initial_sidebar_state='auto',
                   menu_items=None)

st.title('Automated Financial Research by AI with Planning & Reasoning')


st.write('__RESEARCH OBJECTIVE__:')

if 'objective' not in st.session_state:
    st.session_state.objective: str = DEFAULT_OBJECTIVE

st.session_state.objective: str = st.text_area(label='Financial Research Objective',
                                               value=st.session_state.objective,
                                               height=9,
                                               max_chars=None,
                                               key=None,
                                               help='Financial Research Objective',
                                               on_change=None, args=None, kwargs=None,
                                               placeholder='Financial Research Objective',
                                               disabled=False,
                                               label_visibility='collapsed')

if 'company' not in st.session_state:
    st.session_state.company: str = COMPANIES[0]

st.session_state.company: str = st.selectbox(label='Watchlist',
                                             options=COMPANIES,
                                             index=COMPANIES.index(st.session_state.company),
                                             # format_func=None,
                                             key=None,
                                             help='Company',
                                             on_change=None, args=None, kwargs=None,
                                             placeholder='Company',
                                             disabled=False,
                                             label_visibility='visible')

webpages_to_incl: str = st.text_area(label='Sources to Include in Research',
                                     value='',
                                     height=9,
                                     max_chars=None,
                                     key=None,
                                     help='Sources to Include in Research',
                                     on_change=None, args=None, kwargs=None,
                                     placeholder='Sources to Include in Research',
                                     disabled=False,
                                     label_visibility='visible')


if st.button(label=f'__RESEARCH & RECOMMEND__: _{st.session_state.company}_',
             key=None,
             on_click=None, args=None, kwargs=None,
             type='primary',
             disabled=False,
             use_container_width=False):
    for url in (i.strip() for i in webpages_to_incl.split('\n')):
        if url:
            br = Browser()
            br.set_handle_robots(False)
            br.open(url)
            st.write(f'_Reading "{br.title()}"..._')
            converter.convert(source=url,
                              target=f'{get_or_create_cached_dir_path(st.session_state.company)}/{br.title()}.pdf',
                              timeout=0.1,
                              install_driver=False)

    solution: str = solve(st.session_state.objective, st.session_state.company)
    st.write(solution)
