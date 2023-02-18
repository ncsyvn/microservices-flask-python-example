# -*- coding: utf-8 -*-

from flask import Flask
from auth_app.api.helper import CONFIG
from auth_app.extensions import logger, db, migrate

def create_app(config_object=CONFIG):
    """
    Init App
    :param config_object:
    :return:
    """
    app = Flask(__name__, static_url_path="", static_folder="./static-files")
    app.config.from_object(config_object)
    register_extensions(app)
    return app


def register_extensions(app):
    """
    Init extension
    :param app:
    :return:
    """

    db.app = app
    db.init_app(app)  # SQLAlchemy
    # jwt.init_app(app)
    migrate.init_app(app, db)
