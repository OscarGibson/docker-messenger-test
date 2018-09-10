# app/__init__.py

import os

from flask import Flask, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_mail import Mail
from flask_marshmallow import Marshmallow

from helpers.functions.url_rules import UrlRules

import importlib


# instantiate the extensions
db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
mail = Mail()
url_rules = UrlRules()
marsh_mallow = Marshmallow()


def create_app(env= 'development'):

    # instantiate the app
    app = Flask(__name__)

    # enable CORS
    CORS(app)

    # set config
    # app_settings = os.getenv('APP_SETTINGS')
    # app.config.from_object(app_settings)

    config = importlib.import_module('src.settings.%s' % env)

    config_list = {}
    [config_list.update({key : getattr(config, key)}) for key in dir(config) if str(key)[0] != '_']
    app.config.update(**config_list)

    # set up extensions
    db.init_app(app)
    bcrypt.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)
    url_rules.init_app(app)
    marsh_mallow.init_app(app)

    # init urls
    from app.api.v1.auth import urls as auth_urls
    from app.api.v1.users import urls as users_urls

    auth_urls.add_rules()
    users_urls.add_rules()

    return app