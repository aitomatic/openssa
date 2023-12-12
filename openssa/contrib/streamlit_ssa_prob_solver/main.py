import os
from pathlib import Path
import sys

import streamlit as st


sys.path.insert(1, str(Path(__file__).parent.parent.parent.parent))


st.title('SSA-Powered Problem Solvers')

st.subheader('Configuration')

st.session_state['LEPTON_API_KEY']: str | None = \
    st.text_input(label='Lepton API Key',
                  value=st.session_state.get('LEPTON_API_KEY'),
                  max_chars=None,
                  type='password',
                  help='Lepton API Key (obtainable at dashboard.lepton.ai)',
                  autocomplete=None,
                  on_change=None, args=None, kwargs=None,
                  placeholder='Lepton API Key (obtainable at dashboard.lepton.ai)',
                  disabled=False,
                  label_visibility='visible')

if st.session_state['LEPTON_API_KEY']:
    os.environ['LEPTON_API_KEY']: str = st.session_state['LEPTON_API_KEY']
