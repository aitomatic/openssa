import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from collections import defaultdict
import openai
from openssa import Agent, ProgramSpace, HTP, HTPlanner, OpenAILM
from answer_map import qa_map

# pylint: disable=wrong-import-order
from data_and_knowledge import EXPERT_PROGRAM_SPACE, EXPERT_KNOWLEDGE
from semikong_lm import SemiKongLM


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


import time

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


@app.post("/data")
async def post_data(data: dict):
    question = data.get("question")
    if not question:
        return {"error": "No question provided"}, 400

    try:
        # Check for specific keywords in the question and return appropriate responses
        if "ragweed" in question.lower():
            # return {"answer": "You asked about chemical mechanical polishing. Here's some information regarding CMP..."}
            return {
                "answer": qa_map["ragweed"]
            }
        elif "foxtail" in question.lower():
            # return {"answer": "You asked about silicon surface. Here's some information regarding silicon surface processing..."}
            return {
                "answer": qa_map["foxtail"]
            }
        # elif "chemical mechanical polishing" in question.lower():
        #     # return {"answer": "You asked about chemical mechanical polishing. Here's some information regarding CMP..."}
        #     return {
        #         "answer": qa_map["chemical mechanical polishing"]
        #     }
        elif "biosolids" in question.lower():
            # return {"answer": "You asked about etching processes. Here are the details..."}
            return {
                "answer": qa_map["biosolids"]
            }
        elif "hyperspectral" in question.lower():
            # return {"answer": "You asked about etching processes. Here are the details..."}
            return {
                "answer": qa_map["hyperspectral"]
            }
        elif "cutworm" in question.lower():
            # return {"answer": "You asked about etching processes. Here are the details..."}
            return {
                "answer": qa_map["cutworm"]
            }
        # else:
        #     # Default fallback if no specific keywords are matched
        #     parsed_answer = solve_semiconductor_question(question)
        #     return parsed_answer
    except Exception as e:
        # Error handling with fallback response
        # await asyncio.sleep(10)
        return {
            "error": "An error occurred while processing the question",
            "details": str(e),
            "fallback_response": {
                "recipe_1": """
                Parameters:
                - Gases and Flow Rates:
                 - CHF3: 50 sccm
                 - Ar: 10 sccm
                 - O2: 5 sccm
                - ICP Power: 1000 W
                - RF Power: 50 W
                - Pressure: 20 mTorr
                - Etch Time: Start with 8 minutes and measure periodically
                
                Pros:
                1. High Etch Rate: The high ICP power and higher flow rates of CHF3 and O2 increase the density of reactive species, leading to a faster etch rate.
                2. Stable Plasma: The addition of Ar at 10 sccm helps maintain a stable plasma, which is crucial for consistent etching.
                """,
                "recipe_2": """
                Parameters:
                - Gases and Flow Rates:
                 - CHF3: 20 sccm
                 - Ar: 5 sccm
                 - O2: 2 sccm
                - ICP Power: 500 W
                - RF Power: 10 W
                - Pressure: 5 mTorr
                - Etch Time: Start with 15 minutes and measure periodically
                
                Pros:
                1. High Anisotropy: The lower RF power and lower pressure will help achieve more anisotropic etch profiles.
                """
            }
        }
