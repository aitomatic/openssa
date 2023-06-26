from config import Config
from flask import Flask

# Import yourproject_root model here
from models import test

app = Flask(__name__)

import routes

if __name__ == '__main__':
    app.run(debug=Config.DEBUG, host='0.0.0.0', port=8080)
