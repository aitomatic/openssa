# pylint: disable=duplicate-code
# routes.py
import os
import uuid
import logging
import tempfile
from werkzeug.utils import secure_filename
from flask import render_template, request, Blueprint, session
from flask import Flask, jsonify
from openssm import (
    logger,
    Logs,
    BaseSSM,
    OpenAIGPT3CompletionSSM, OpenAIGPT3ChatCompletionSSM,
    Falcon7bSSM,
    LlamaIndexSSM
)


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
    'llama_index': LlamaIndexSSM(),
    'gpt3_completion': OpenAIGPT3CompletionSSM(),
    'gpt3_chat_completion': OpenAIGPT3ChatCompletionSSM(),
    'falcon7b': Falcon7bSSM(),
}


@routes.route('/discuss', methods=['POST'])
@Logs.do_log_entry_and_exit({'request': request}, the_logger=logger)
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

    response = ssm.discuss(session['conversation_id'], user_input)
    response = response[0]
    # response = html.escape(response)  # Sanitize the response
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


@routes.route('/upload', methods=['POST'])
@Logs.do_log_entry_and_exit({'request': request}, the_logger=logger, log_level=logging.INFO)
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file:
        if not allowed_file(file.filename):
            return jsonify({'error': 'File type not allowed'}), 400

        # Create a temporary directory using tempfile.mkdtemp()
        upload_folder = tempfile.mkdtemp()
        logger.debug("upload_folder: %s", upload_folder)

        filename = secure_filename(file.filename)
        file.save(os.path.join(upload_folder, filename))

        llama_index_ssm = ssms['llama_index']
        if llama_index_ssm is None:
            return jsonify({'error': 'llama_index SSM unavailable'}), 500

        llama_index_ssm.read_directory(upload_folder)

        return jsonify({'filename': filename}), 200

    return jsonify({'error': 'Unexpected error occurred'}), 500


@routes.route('/knowledge', methods=['POST'])
@Logs.do_log_entry_and_exit({'request': request}, the_logger=logger)
def receive_knowledge():
    knowledge_text = request.form.get('knowledge')

    if not knowledge_text:
        return jsonify({'error': 'No knowledge received'}), 400

    # Store the knowledge_text into your knowledge base here

    # Upon successful storage
    return jsonify({'message': 'Knowledge received successfully'}), 200
