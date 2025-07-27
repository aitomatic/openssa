from collections import defaultdict

import streamlit as st
from loguru import logger

# pylint: disable=wrong-import-order
from agent import get_or_create_agent
from openssa import OpenAILM

TITLE: str = 'OpenSSA: Semiconductor Industry-Specific Agent leveraging SemiKong LM'

st.set_page_config(page_title=TITLE,
                   page_icon=None,
                   layout='wide',
                   initial_sidebar_state='auto',
                   menu_items=None)

st.title(body=TITLE, anchor=None, help=None)

DEFAULT_PROBLEM: str = (
    'I am trying to etch 2 μm of PECVD SiO2 using a ~4 μm PR mask to create a pattern of 20 * 60 μm. '
    '\n'
    'I am using the Oxford ICP-RIE Plasmalab System 100. '
    '\n'
    'Recommend me 2 recipes and their pros & cons.'
)

st.write('__PROBLEM/QUESTION__:')

if 'typed_problem' not in st.session_state:
    st.session_state.typed_problem: str = DEFAULT_PROBLEM

st.session_state.typed_problem: str = st.text_area(label='Problem/Question',
                                                   value=st.session_state.typed_problem,
                                                   height=68,
                                                   max_chars=None,
                                                   key=None,
                                                   help='Problem/Question',
                                                   on_change=None, args=None, kwargs=None,
                                                   placeholder='Problem/Question',
                                                   disabled=False,
                                                   label_visibility='collapsed')

if 'semikong_agent_solutions' not in st.session_state:
    st.session_state.semikong_agent_solutions: defaultdict[str, str] = defaultdict(str)

st.subheader('SEMICONDUCTOR INDUSTRY-SPECIFIC AGENT')
st.subheader('_using `SemiKong` LM_')

if st.button(label='SOLVE',
             on_click=None, args=None, kwargs=None,
             type='primary',
             disabled=False,
             use_container_width=False):
    with st.spinner(text='_SOLVING..._'):
        logger.level('DEBUG')

        st.session_state.semikong_agent_solutions[st.session_state.typed_problem]: str = \
            get_or_create_agent(use_semikong_lm=False).solve(problem=st.session_state.typed_problem)


def parse_recipe_text(text: str) -> dict[str, str]:
    # Initialize an empty dictionary to store the parsed data
    parsed_data = {"recipe_1": "", "recipe_2": "", "agent_advice": ""}

    # Split the text by lines
    lines = text.split("\n")

    # Initialize a variable to keep track of the current section
    current_section = None

    # Loop through each line
    for line in lines:
        # Check if the line indicates the start of a new section
        if "recipe_1:" in line:
            current_section = "recipe_1"
        elif "recipe_2:" in line:
            current_section = "recipe_2"
        elif "agent_advice:" in line:
            current_section = "agent_advice"
        elif current_section:
            # If we are in a section, append the line to the corresponding key in the dictionary
            parsed_data[current_section] += line + "\n"

    # Remove any trailing newlines from the values
    parsed_data = {key: value.strip() for key, value in parsed_data.items()}

    return parsed_data


if (solution := st.session_state.semikong_agent_solutions[st.session_state.typed_problem]):
    solution = OpenAILM.from_defaults().get_response(
        prompt=f"""{solution} \n\n Please help me parse the above text into this format:\n
         recipe_1: Show the recipe 1 here\n
         recipe_2: Show the recipe 2 here\n
         agent_advice: Show the agent's general considerations here\n
         DO NOT forget the key and DO NOT change the key format.
""",
        history=[
            {"role": "system",
             "content": "You are an expert in parsing text into a specific format. Please help me with this task."},
        ]
    )

    # solution = parse_recipe_text(solution)

    st.markdown(body=solution)
