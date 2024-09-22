from flask import Flask
from flask_pymongo import PyMongo
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()
# Print the environment variables to check if they are loaded correctly
print(f"MONGO_URI: {os.getenv('MONGO_URI')}")
print(f"SECRET_KEY: {os.getenv('SECRET_KEY')}")
mongo = PyMongo()

def create_app():
    app = Flask(__name__)

    # Load configuration from environment variables
    app.config['MONGO_URI'] = os.getenv('MONGO_URI')
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

    # Initialize MongoDB
    mongo.init_app(app)

    from .routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
