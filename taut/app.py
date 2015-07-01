#!/usr/bin/env python
# coding: utf-8

import os
import hmac
import rollbar
import rollbar.contrib.flask
from hashlib import sha1
from werkzeug.contrib.cache import SimpleCache
from flask import Flask, g, got_request_exception
from flask.ext.babel import Babel, format_datetime
from flask.ext.assets import Environment, Bundle
from .models import db
from .routes import index, settings, media, bookmark, developer
from .routes import admin, api
from .helpers.account import load_current_user
from .helpers.value import thumb, human_time, url_for_media_detail

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
    register_assets(app)
    register_jinja2(app)
    register_database(app)
    register_cache(app)
    register_route(app)

    return app

def register_hook(app):
    @app.before_first_request
    def init_rollbar():
        if app.config['ROLLBAR']['enable']:
            rollbar.init(
                app.config['ROLLBAR']['access_token'],
                'production',
                root=os.path.dirname(os.path.realpath(__file__)),
                allow_logging_basic_config=False
            )
            got_request_exception.connect(rollbar.contrib.flask.report_exception, app)

    @app.before_request
    def current_user():
        g.user = load_current_user()

def register_babel(app):
    babel = Babel(app)

def register_assets(app):
    assets = Environment()
    assets.init_app(app)

def register_jinja2(app):
    @app.template_filter('timeago')
    def timeago(value):
        return human_time(value)

    @app.template_filter('dateformat')
    def dateformat(_datetime, format='yyyy-MM-dd H:mm'):
        return format_datetime(_datetime, format)

    @app.template_filter('thumbor')
    def thumbor(url, width, height, unsafe=False):
        return thumb(url, width, height, unsafe)

    @app.template_filter('remove_url')
    def remove_url(text):
        import re
        return re.sub(r'\w+:\/{2}[\d\w-]+(\.[\d\w-]+)*(?:(?:\/[^\s/]*))*', '', text, flags=re.MULTILINE)

    @app.template_filter('remove_newline')
    def remove_newline(text):
        return ''.join(text.splitlines()).rstrip('\r\n')

    @app.context_processor
    def utility_processor():
        return dict(url_for_media_detail=url_for_media_detail)

def register_database(app):
    db.init_app(app)
    db.app = app

def register_cache(app):
    app.cache = SimpleCache()

def register_route(app):
    app.register_blueprint(admin.account.blueprint, url_prefix='/admin/account')
    app.register_blueprint(admin.list_media.blueprint, url_prefix='/admin/list-media')
    app.register_blueprint(admin.list_tweet.blueprint, url_prefix='/admin/list-tweet')
    app.register_blueprint(admin.list_user.blueprint, url_prefix='/admin/list-user')
    app.register_blueprint(admin.main.blueprint, url_prefix='/admin')
    app.register_blueprint(api.media.blueprint, url_prefix='/api/media')
    app.register_blueprint(api.main.blueprint, url_prefix='/api')
    app.register_blueprint(developer.blueprint, url_prefix='/developer')
    app.register_blueprint(bookmark.blueprint, url_prefix='/bookmark')
    app.register_blueprint(media.blueprint, url_prefix='/media')
    app.register_blueprint(settings.blueprint, url_prefix='/settings')
    app.register_blueprint(index.blueprint, url_prefix='')
