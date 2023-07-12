import os


class Config:
    """
    This class is used to store config setings, as well as
    secrets, such as API keys, tokens, etc.
    By default, they come from documented environment variables.
    But the user can override them by setting them directly
    in the Config object.
    """

    _dummy = "value is not set"

    DEBUG = False

    # get OPENAI_API_KEY from environment variable
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY') or _dummy

    # get HUGGING_FACE_HUB_TOKEN from environment variable
    HUGGING_FACE_HUB_TOKEN = os.environ.get('HUGGING_FACE_HUB_TOKEN') or _dummy

    # Falcon7b server token (HuggingFace’s, or our own server)
    FALCON7B_SERVER_TOKEN = os.environ.get(
        'FALCON7B_SERVER_TOKEN') or HUGGING_FACE_HUB_TOKEN

    # Falcon7b server URL (HuggingFace’s, or our own server)
    FALCON7B_MODEL_URL = os.environ.get('FALCON7B_MODEL_URL')
