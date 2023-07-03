from config import Config
from flask import Flask

from routes import routes

app = Flask(__name__)
app.register_blueprint(routes)

# For "python app.py"
if __name__ == '__main__':
    app.run(debug=Config.DEBUG, host='0.0.0.0', port=8080)