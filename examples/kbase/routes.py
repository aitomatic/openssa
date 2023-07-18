# pylint: disable=duplicate-code
# routes.py
import os
import uuid
import html
from werkzeug.utils import secure_filename

from flask import render_template, request, Blueprint, session
from flask import Flask, redirect, url_for, jsonify

from openssm.core.ssm.abstract_ssm import AbstractSSM

from openssm.core.ssm.openai_ssm import GPT3CompletionSSM
from openssm.core.ssm.openai_ssm import GPT3ChatCompletionSSM
from openssm.core.ssm.huggingface_ssm import Falcon7bSSM
# from openssm.core.ssm.huggingface_ssm import Falcon7bSSMLocal


# Create a new blueprint
routes = Blueprint('routes', __name__)

app = Flask(__name__)

UPLOAD_FOLDER = '/path/to/the/uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


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

    response = ssm.discuss(session['conversation_id'], user_input)[0]
    response = html.escape(response)  # Sanitize the response
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


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/upload', methods=['POST'])
def old_upload_file():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return redirect(url_for('uploaded_file',
                                filename=filename))
    return redirect(url_for('index'))


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return jsonify({'filename': filename}), 200
    return jsonify({'error': 'Unexpected error occurred'}), 500


@app.route('/knowledge', methods=['POST'])
def old_receive_knowledge():
    # knowledge_text = request.form['knowledge']
    # Store the knowledge_text into your knowledge base here
    return redirect(url_for('index'))


@app.route('/knowledge', methods=['POST'])
def receive_knowledge():
    knowledge_text = request.form.get('knowledge')

    if not knowledge_text:
        return jsonify({'error': 'No knowledge received'}), 400

    # Store the knowledge_text into your knowledge base here

    # Upon successful storage
    return jsonify({'message': 'Knowledge received successfully'}), 200
