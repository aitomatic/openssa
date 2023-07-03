# routes.py
from app import app
from flask import render_template, Flask, request
from dotenv import load_dotenv
import openai

from ssms.semiconductor_ssm import semi_ald_ssm

load_dotenv()


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    model = data['model']
    messages = data['messages']
    print(f'MESSAGES: {messages}')
    response = semi_ald_ssm.process_request(messages[-1]['content'])
    print(f'RESPONSE: {response}')
    return {
        'choices': [
            {
                'index': 0,
                'message': {'role': 'assistant', 'content': response}
            },
        ],
    }, 200
