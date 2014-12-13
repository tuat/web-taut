#!/usr/bin/env python

import os
import hmac
from hashlib import sha1
from base64 import urlsafe_b64encode
from datetime import datetime
from flask import Flask, g
from flask.ext.babel import Babel, format_datetime
from .models import db
from .routes import index, settings, media, bookmark, developer
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
    register_babel(app)
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

def register_babel(app):
    babel = Babel(app)

def register_celery(app):
    app.celery = make_celery(app)

def register_celery_beat(app):
    from .tasks.schedule import fetch_lists

def register_jinja2(app):
    @app.template_filter('timeago')
    def timeago(value):
        now = datetime.utcnow()
        delta = now - value

        if delta.days > 365:
            return '{0} years ago'.format(delta.days / 365)
        if delta.days > 30:
            return '{0} months ago'.format(delta.days / 30)
        if delta.days > 0:
            return '{0} days ago'.format(delta.days)
        if delta.seconds > 3600:
            return '{0} hours ago'.format(delta.seconds / 3600)
        if delta.seconds > 60:
            return '{0} minutes ago'.format(delta.seconds / 60)
        return 'just now'

    @app.template_filter('dateformat')
    def dateformat(_datetime, format='yyyy-MM-dd H:mm'):
        return format_datetime(_datetime, format)

    @app.template_filter('thumbor')
    def thumbor(url, width, height, unsafe=False):
        url_parts = "{0}x{1}/{2}".format(width, height, url.replace("http://",""))

        if unsafe:
            return "{0}/unsafe/{1}".format(app.config.get('THUMBOR_BASE_URL'), url_parts)
        else:
            sign_code = urlsafe_b64encode(hmac.new(app.config.get('THUMBOR_SECURITY_KEY'), url_parts, sha1).digest())

            return "{0}/{1}/{2}".format(app.config.get('THUMBOR_BASE_URL'), sign_code, url_parts)

def register_database(app):
    db.init_app(app)
    db.app = app

def register_route(app):
    app.register_blueprint(admin.list_media.blueprint, url_prefix='/admin/list-media')
    app.register_blueprint(admin.list_tweet.blueprint, url_prefix='/admin/list-tweet')
    app.register_blueprint(admin.list_user.blueprint, url_prefix='/admin/list-user')
    app.register_blueprint(admin.main.blueprint, url_prefix='/admin')
    app.register_blueprint(developer.blueprint, url_prefix='/developer')
    app.register_blueprint(bookmark.blueprint, url_prefix='/bookmark')
    app.register_blueprint(media.blueprint, url_prefix='/media')
    app.register_blueprint(settings.blueprint, url_prefix='/settings')
    app.register_blueprint(index.blueprint, url_prefix='')
