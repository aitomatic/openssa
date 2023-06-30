import os,sys,openai

# Add the project lib directory to PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../ssm')))


class Config:
    DEBUG = True

    # other config variables...
    openai.api_key = os.getenv("OPENAI_API_KEY")
