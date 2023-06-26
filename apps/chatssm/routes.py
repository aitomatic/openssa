# routes.py
from app import app
from flask import render_template, Flask, request
import openai

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    model = data['model']
    messages = data['messages']
    response = openai.ChatCompletion.create(model=model, messages=messages)
    return response.to_dict(), 200

