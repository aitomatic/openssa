import os
from openssm import Config


# Logging.set_log_level(logging.INFO)

# Flask config variables
Config.FLASK_SECRET_KEY = os.environ.get(
    'FLASK_SECRET_KEY') or '_5#8z\n\xec]/'

# other config variables...

# These are already automatically done in the openssm/core/config.py file
# Override them here if you want to use different values
# Config.OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
# Config.OPENAI_API_URL = os.getenv("OPENAI_API_URL")
# Config.FALCON7B_API_URL = os.getenv("FALCON7B_API_URL")
# Config.FALCON7B_API_KEY = os.getenv("FALCON7B_API_KEY") or
# Config.HUGGING_FACE_HUB_TOKEN = os.getenv("HUGGING_FACE_HUB_TOKEN")

# pylint: disable=wrong-import-order
# pylint: disable=wrong-import-position
# pylint: disable=unused-import
import config_secrets
