import os
from openssm import Config


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

#
# config_secrets.py is auto-created by Makefile for the purpose of execution
# and deploying to secure hosting servers. It must be .gitignore’d so as to avoid
# leaking secrets to GitHub. Makefile reads environment variables and hardcodes these
# values into config_secrets.py just prior to deployment.
#
# pylint: disable=wrong-import-order
# pylint: disable=wrong-import-position
# pylint: disable=unused-import
import config_secrets
