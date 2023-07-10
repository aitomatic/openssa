# routes.py
import uuid

from flask import render_template, request, Blueprint, session

from openssm.core.ssm.abstract_ssm import AbstractSSM

from openssm.core.ssm.openai_ssm import GPT3CompletionSSM
from openssm.core.ssm.openai_ssm import GPT3ChatCompletionSSM
from openssm.core.ssm.huggingface_ssm import Falcon7bSSM
# from openssm.core.ssm.huggingface_ssm import Falcon7bSSMLocal

# Create a new blueprint
routes = Blueprint('routes', __name__)


@routes.route('/')
def home():
    return render_template('index.html')


ssms = {
    'gpt3_completion': GPT3CompletionSSM(),
    'gpt3_chat_completion': GPT3ChatCompletionSSM(),
    'falcon7b': Falcon7bSSM(),
    # 'falcon7b_local': Falcon7bSSMLocal(),
}


@routes.route('/discuss', methods=['POST'])
def discuss():
    if 'conversation_id' not in session:
        session['conversation_id'] = str(uuid.uuid4())

    data = request.get_json()

    sysmsgs = []

    model = data['model']
    sysmsgs.append(f'MODEL: {model}')

    ssm: AbstractSSM = ssms[model] or ssms['gpt3_chat_completion']

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
