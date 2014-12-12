#!/usr/bin/env python

import os
from flask import Flask, g
from .models import db
from .routes import index
from .routes import admin
from .tasks import make_celery
from .helpers.account import load_current_user

def create_app(config=None):
    app = Flask(__name__, template_folder='views')
    app.static_folder = os.path.abspath('static')

    app.config.from_pyfile('configs/default.py')

    production_config = os.path.join(os.path.dirname(__file__), 'configs/production.py')
    if os.path.exists(production_config):
        app.config.from_pyfile(production_config)

    if isinstance(config, dict):
        app.config.update(config)
    elif config:
        app.config.from_pyfile(os.path.abspath(config))

    register_hook(app)
    register_celery(app)
    register_celery_beat(app)
    register_jinja2(app)
    register_database(app)
    register_route(app)

    return app

def register_hook(app):
    @app.before_request
    def current_user():
        g.user = load_current_user()

def register_celery(app):
    app.celery = make_celery(app)

def register_celery_beat(app):
    from .tasks.schedule import fetch_lists

def register_jinja2(app):
    pass

def register_database(app):
    db.init_app(app)
    db.app = app

def register_route(app):
    app.register_blueprint(admin.list_user.blueprint, url_prefix='/admin/list-user')
    app.register_blueprint(admin.main.blueprint, url_prefix='/admin')
    app.register_blueprint(index.blueprint, url_prefix='')
