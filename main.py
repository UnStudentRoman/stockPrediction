from flask import Flask
from flask_cors import CORS
from api_handler import api_blueprint
from logging_handler import setup_logging
from os import makedirs


def create_app():
    app = Flask(__name__)
    CORS(app)  # Enable CORS for frontend communication

    # Setup logging
    setup_logging()

    # Register blueprints
    app.register_blueprint(api_blueprint)

    # Ensure required directories exist
    makedirs("uploads", exist_ok=True)
    makedirs("logs", exist_ok=True)
    makedirs("database", exist_ok=True)

    return app


if __name__ == "__main__":
    App = create_app()
    App.run(debug=True, host='0.0.0.0', port=5000)
