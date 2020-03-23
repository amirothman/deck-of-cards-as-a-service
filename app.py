from logging import Formatter
from logging.handlers import RotatingFileHandler

from flask import Flask

from api import api_blueprint


def set_logger(app):
    handler = RotatingFileHandler(
        app.config["LOG_PATH"], maxBytes=512 * 1024 * 1024, backupCount=10
    )
    formatter = Formatter("[%(levelname)s] %(asctime)s - %(name)s - %(message)s")
    handler.setFormatter(formatter)
    app.logger.addHandler(handler)


class Config:
    LOG_PATH = "app.log"


def create_app():
    """Prepare and return a new instance of the Flask app."""
    app = Flask(__name__)
    app.config.from_object(Config)
    set_logger(app)
    register_blueprints(app)

    return app


def register_blueprints(app):
    """Attach API routes to the application."""
    app.register_blueprint(api_blueprint)
