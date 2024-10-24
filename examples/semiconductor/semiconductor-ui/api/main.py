import logging
import os
import time
from collections import defaultdict

import openai
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# pylint: disable=wrong-import-order
from data_and_knowledge import EXPERT_PROGRAM_SPACE, EXPERT_KNOWLEDGE
from openssa import Agent, ProgramSpace, HTP, HTPlanner, OpenAILM
from semikong_lm import SemiKongLM

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)


def get_or_create_agent(
        use_semikong_lm: bool = True, max_depth=2, max_subtasks_per_decomp=4
) -> Agent:
    lm = (SemiKongLM if use_semikong_lm else OpenAILM).from_defaults()

    program_space = ProgramSpace(lm=lm)
    if EXPERT_PROGRAM_SPACE:
        for program_name, htp_dict in EXPERT_PROGRAM_SPACE.items():
            htp = HTP.from_dict(htp_dict)
            program_space.add_or_update_program(
                name=program_name, description=htp.task.ask, program=htp
            )

    return Agent(
        program_space=program_space,
        programmer=HTPlanner(
            lm=lm, max_depth=max_depth, max_subtasks_per_decomp=max_subtasks_per_decomp
        ),
        knowledge={EXPERT_KNOWLEDGE} if EXPERT_KNOWLEDGE else None,
        resources={},
    )


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.environ.get("FRONTEND_URL", "http://localhost:4000")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = openai.OpenAI(api_key=os.environ["OPENAI_API_KEY"])


def call_gpt(prompt):
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": "You are an expert in parsing text into a specific format. Please help me with this task.",
            },
            {"role": "user", "content": prompt},
        ],
    )
    return response.choices[0].message.content


def parse_recipe_text(text):
    parsed_data = {"recipe_1": "", "recipe_2": "", "agent_advice": ""}
    lines = text.split("\n")
    current_section = None

    for line in lines:
        if "recipe_1:" in line:
            current_section = "recipe_1"
        elif "recipe_2:" in line:
            current_section = "recipe_2"
        elif "agent_advice:" in line:
            current_section = "agent_advice"
        elif current_section:
            parsed_data[current_section] += line + "\n"

    parsed_data = {key: value.strip() for key, value in parsed_data.items()}
    return parsed_data


def solve_semiconductor_question(question):
    start = time.time()
    solutions = defaultdict(str)

    solutions[question] = get_or_create_agent(use_semikong_lm=True).solve(
        problem=question
    )

    print(f"get_or_create_agent taken: {time.time() - start}")
    start = time.time()

    solution = solutions[question]
    solution = solution.replace("$", r"\$")

    prompt = f"""{solution} \n\n Please help me parse the above text into this format:\n
         recipe_1: Show the recipe 1 here\n
         recipe_2: Show the recipe 2 here\n
         agent_advice: Show the agent's general considerations here\n
         DO NOT forget the key and DO NOT change the key format.
    """

    solution = call_gpt(prompt)
    print(f"call_gpt taken: {time.time() - start}")
    start = time.time()
    parsed_solution = parse_recipe_text(solution)
    print(f"parse_recipe_text taken: {time.time() - start}")
    return parsed_solution


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/data")
async def get_data():
    return {"data": "data"}


DEFAULT_ANSWER = """
{'recipe_1': 'Parameters:\n- Gases and Flow Rates:\n - CHF3: 50 sccm\n - Ar: 10 sccm\n - O2: 5 sccm\n- ICP Power: 1000 W\n- RF Power: 50 W\n- Pressure: 20 mTorr\n- Etch Time: Start with 8 minutes and measure periodically\n\nPros:\n1. High Etch Rate: The high ICP power and higher flow rates of CHF3 and O2 increase the density of reactive species, leading to a faster etch rate.\n2. Stable Plasma: The addition of Ar at 10 sccm helps maintain a stable plasma, which is crucial for consistent etching.\n3. Improved Volatility: The higher O2 flow rate enhances the volatility of etch products, improving overall etch efficiency.\n\nCons:\n1. Physical Damage: The high ICP power and RF power can lead to more physical damage to the PR mask and underlying layers due to increased ion bombardment.\n2. Less Anisotropic Profiles: Higher RF power may result in less anisotropic etch profiles, which could be problematic for applications requiring precise vertical etching.\n3. Higher Pressure: The higher pressure may reduce the mean free path of ions, potentially affecting the directionality of the etch.', 'recipe_2': 'Parameters:\n- Gases and Flow Rates:\n - CHF3: 20 sccm\n - Ar: 5 sccm\n - O2: 2 sccm\n- ICP Power: 500 W\n- RF Power: 10 W\n- Pressure: 5 mTorr\n- Etch Time: Start with 15 minutes and measure periodically\n\nPros:\n1. High Anisotropy: The lower RF power and lower pressure will help achieve more anisotropic etch profiles, which is essential for applications requiring precise vertical etching.\n2. Reduced Physical Damage: Lower ICP and RF power reduce the risk of physical damage to the PR mask and underlying layers, making this set suitable for delicate structures.\n3. Directional Etching: The lower pressure improves the directionality of the etch by reducing the number of collisions between ions and neutral species.\n\nCons:\n1. Lower Etch Rate: The lower ICP power and reduced flow rates of CHF3 and O2 will result in a slower etch rate, requiring longer etch times to achieve the desired depth.\n2. Plasma Stability: The lower flow rate of Ar may make it more challenging to maintain a stable plasma, which could affect the consistency of the etch process.\n3. Process Control: The lower pressure and power settings require more precise control of the process parameters to maintain stability and achieve the desired etch profile.', 'agent_advice': '- Etch Rate and Uniformity: Regularly measure the etch depth to ensure uniformity across the wafer. Adjust the etch time accordingly.\n- End-Point Detection: Utilize optical emission spectroscopy (OES) or interferometry if available on the Plasmalab System 100 to accurately determine the end-point of the etch process.\n- Safety Procedures: Always follow safety protocols when handling gases and operating the ICP RIE system. Confirm with the facility manager that the chosen recipe is compatible with the equipment.\n\nBy starting with these recipes and making necessary adjustments based on periodic measurements and observations, you should be able to achieve the desired etch depth and profile for your SiO2 pattern.\n```'}
    """


@app.post("/data")
async def post_data(data: dict):
    question = data.get("question")
    if not question:
        return {"error": "No question provided"}, 400

    try:
        parsed_answer = solve_semiconductor_question(question)
    except ValueError:
        logger.exception("Value error")
        return DEFAULT_ANSWER
    except RuntimeError:
        logger.exception("Runtime error")
        return DEFAULT_ANSWER
    return parsed_answer
