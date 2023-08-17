# pylint: disable=duplicate-code
# routes.py
import uuid

from flask import render_template, request, Blueprint, session

from openssm import (
    BaseSSM,
    OpenAIGPT3CompletionSSM, OpenAIGPT3ChatCompletionSSM,
    Falcon7bSSM
)

# Create a new blueprint
routes = Blueprint('routes', __name__)


@routes.route('/')
def home():
    return render_template('index.html')


ssms = {
    'gpt3_completion': OpenAIGPT3CompletionSSM(),
    'gpt3_chat_completion': OpenAIGPT3ChatCompletionSSM(),
    'falcon7b': Falcon7bSSM(),
}


@routes.route('/discuss', methods=['POST'])
def discuss():
    if 'conversation_id' not in session:
        session['conversation_id'] = str(uuid.uuid4())

    data = request.get_json()

    sysmsgs = []

    model = data['model']
    sysmsgs.append(f'MODEL: {model}')

    ssm: BaseSSM = ssms[model] or ssms['gpt3_chat_completion']

    message = data['message']
    sysmsgs.append(f'MESSAGE: {message}')

    user_input = [{'role': 'user', 'content': message}]

    response = ssm.discuss(session['conversation_id'], user_input)[0]
    sysmsgs.append(f'RESPONSE: {response}')

    return {
        'choices': [
            {
                'index': 0,
                'message': response,
                'syslog': sysmsgs
            },
        ],
    }, 200
