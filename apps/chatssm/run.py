from config import Config
from app import app

if __name__ == '__main__':
    app.run(debug=Config.DEBUG, host='0.0.0.0', port=8080)
