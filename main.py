from flask import Flask
from flask_cors import CORS
from api_handler import api_blueprint, swagger_ui_blueprint
from logging_handler import setup_logging
from os import makedirs
from config import SWAGGER_URL


def create_app():
    # Ensure required directories exist
    makedirs("uploads", exist_ok=True)
    makedirs("logs", exist_ok=True)
    makedirs("database", exist_ok=True)

    app = Flask(__name__)
    CORS(app)  # Enable CORS for frontend communication

    # Setup logging
    setup_logging()

    # Register blueprints
    app.register_blueprint(api_blueprint)
    # Register the Swagger UI blueprint
    app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)

    return app


if __name__ == "__main__":
    App = create_app()
    App.run(debug=False, host='0.0.0.0', port=5000)
