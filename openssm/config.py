import os


class Config:
    # get OPENAI_API_KEY from environment variable
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')

    # get HUGGING_FACE_HUB_TOKEN from environment variable
    HUGGING_FACE_HUB_TOKEN = os.environ.get('HUGGING_FACE_HUB_TOKEN')

    # Falcon7b server URL (HuggingFace’s, or our own server)
    FALCON7B_MODEL_URL = os.environ.get('FALCON7B_MODEL_URL') 
    FALCON7B_SERVER_TOKEN = os.environ.get('FALCON7B_SERVER_TOKEN') or HUGGING_FACE_HUB_TOKEN