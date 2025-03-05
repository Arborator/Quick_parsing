import os 
from flask_cors import CORS
from app import create_app

from dotenv import load_dotenv

load_dotenv(dotenv_path=".flaskenv", verbose=True)

env = os.getenv("FLASK_ENV")

app = create_app(env)

CORS(app, origins=["https://127.0.0.1:9000"])
if __name__ == '__main__':
    app.run("0.0.0.0", 5000, debug=True)