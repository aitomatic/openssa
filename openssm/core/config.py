import os


class Config:
    # get OPENAI_API_KEY from environment variable
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
