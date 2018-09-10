# app/__init__.py

import os

from flask import Flask, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow

from helpers.functions.url_rules import UrlRules
from helpers.functions import get_config_by_env

import importlib


# instantiate the extensions
db = SQLAlchemy()
migrate = Migrate()
url_rules = UrlRules()
marsh_mallow = Marshmallow()


def create_app(env= 'development'):

    # instantiate the app
    app = Flask(__name__)

    # enable CORS
    CORS(app)

    app.config.update(**get_config_by_env(env))

    # set up extensions
    db.init_app(app)
    migrate.init_app(app, db)
    url_rules.init_app(app)
    marsh_mallow.init_app(app)

    # init urls
    from app.api.v1.projects import urls
    urls.add_rules()

    return app
