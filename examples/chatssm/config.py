import os
import openai


class Config:
    DEBUG = True
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'

    # other config variables...
    openai.api_key = os.getenv("OPENAI_API_KEY")
