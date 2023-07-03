# routes.py
from flask import render_template, request, Blueprint
from openssm.core.ssm.gpt3_ssm import GPT3CompletionSSM, GPT3ChatCompletionSSM

# Create a new blueprint
routes = Blueprint('routes', __name__)


@routes.route('/')
def home():
    return render_template('index.html')


ssms = {
    'gpt3_completion': GPT3CompletionSSM(),
    'gpt3_chat_completion': GPT3ChatCompletionSSM(),
}


@routes.route('/discuss', methods=['POST'])
def discuss():
    data = request.get_json()

    sysmsgs = []

    model = data['model']
    sysmsgs.append(f'MODEL: {model}')

    ssm = ssms[model] or ssms['gpt3_chat_completion']

    message = data['message']
    sysmsgs.append(f'MESSAGE: {message}')

    user_input = [{'role': 'user', 'content': message}]

    response = ssm.discuss("123", user_input)[0]
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
