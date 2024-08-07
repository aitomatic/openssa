import os
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from collections import defaultdict
import openai

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.environ.get("FRONTEND_URL", "http://localhost:4000")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = openai.OpenAI(api_key=os.environ['OPENAI_API_KEY'])

def call_gpt(prompt):
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are an expert in parsing text into a specific format. Please help me with this task."},
            {"role": "user", "content": prompt}
        ]
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
    solutions = defaultdict(str)

    solutions[question] = get_or_create_agent(use_semikong_lm=True).solve(problem=question)

    solution = solutions[question]
    solution = solution.replace('$', r'\$')
    
    prompt = f"""{solution} \n\n Please help me parse the above text into this format:\n
         recipe_1: Show the recipe 1 here\n 
         recipe_2: Show the recipe 2 here\n
         agent_advice: Show the agent's general considerations here\n
         DO NOT forget the key and DO NOT change the key format.
    """
    solution = call_gpt(prompt)
    parsed_solution = parse_recipe_text(solution)
    return parsed_solution

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/data")
async def get_data():
    return {"data": "data"}

@app.post("/data")
async def post_data(request: Request):
    data = await request.json()
    question = data.get('question')
    if not question:
        return {"error": "No question provided"}, 400

    try:
        parsed_answer = solve_semiconductor_question(question)
        return parsed_answer
    except Exception as e:
        logger.error(f"Error solving the question: {e}")
        return {"error": str(e)}, 500

