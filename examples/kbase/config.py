import os
from openssm.config import Config


Config.DEBUG = True

# Flask config variables
Config.FLASK_SECRET_KEY = os.environ.get(
    'FLASK_SECRET_KEY') or '_5#8z\n\xec]/'

# other config variables...

# These are already automatically done in the openssm/core/config.py file
# Override them here if you want to use different values
# Config.OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
# Config.HUGGING_FACE_HUB_TOKEN = os.getenv("HUGGING_FACE_HUB_TOKEN")
# Config.FALCON7B_MODEL_URL = os.getenv("FALCON7B_MODEL_URL")
# Config.FALCON7B_SERVER_TOKEN = os.getenv("FALCON7B_SERVER_TOKEN") or
# Config.HUGGING_FACE_HUB_TOKEN

# pylint: disable=wrong-import-order
# pylint: disable=wrong-import-position
# pylint: disable=unused-import
import config_secrets
