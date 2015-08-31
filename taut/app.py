#!/usr/bin/env python
# coding: utf-8

import os
import hmac
import rollbar
import rollbar.contrib.flask
from hashlib import sha1
from werkzeug.contrib.cache import FileSystemCache
from flask import Flask, g, got_request_exception, render_template, jsonify, request, flash, redirect
from flask.ext.babel import Babel, format_datetime
from flask.ext.assets import Environment, Bundle
from flask.ext.oauthlib.client import OAuth
from flask.ext.jwt import JWT
from .models import db, Account
from .helpers.account import load_current_user
from .helpers.value import thumb, human_time, url_for_media_detail, url_for_bookmark_create, url_for_bookmark_remove

def create_app(config=None, enable_route=True):
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

    register_database(app)
    register_jwt(app)
    register_hook(app)
    register_error(app)
    register_babel(app)
    register_assets(app)
    register_oauth(app)
    register_jinja2(app)
    register_cache(app)

    if enable_route is True:
        register_route(app)

    return app

def register_database(app):
    db.init_app(app)
    db.app = app

    if "USE_PSYCOGREEN" in os.environ:
        db.engine.pool._use_threadlocal = True

def register_jwt(app):
    jwt = JWT(app)

    # curl -X POST -H "Content-Type: application/json" -d '{"username":"<USERNAME>","password":"<PASSWORD>"}' http://localhost:5000/api/auth
    @jwt.authentication_handler
    def authenticate(username, password):
        if '@' in username:
            user = Account.query.filter_by(email=username).first()
        else:
            user = Account.query.filter_by(username=username).first()

        if user and user.password_verify(password):
            return user

    # curl -H "Authorization: Bearer <JWT_TOKEN>" http://localhost:5000/api/media/detail/protected?token=<TOKEN>
    @jwt.user_handler
    def load_user(payload):
        if 'user_id' in payload:
            return Account.query.get(payload['user_id'])

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

    @app.after_request
    def close_db(response):
        db.session.close()
        db.engine.dispose()
        return response

def register_error(app):
    @app.errorhandler(404)
    def page_not_found(e):
        if request.is_xhr or request.path.startswith('/api'):
            return jsonify(status=404, message="Page not found")
        else:
            return render_template('error/404.html'), 404

    @app.errorhandler(500)
    def internet_server_error(e):
        referrer_url = request.referrer

        if referrer_url:
            flash('Somthing went wrong, Please make action again', 'error')

            return redirect(request.referrer)
        else:
            return render_template('error/500.html'), 500;

def register_babel(app):
    babel = Babel(app)

def register_assets(app):
    assets = Environment()
    assets.init_app(app)

def register_oauth(app):
    oauth   = OAuth(app)
    dropbox = oauth.remote_app('dropbox', app_key='DROPBOX')

    app.oauth = oauth
    app.oauth.providers = {
        'dropbox': dropbox
    }

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
        def is_admin():
            return g.user and g.user.role == 'admin'
        return dict(is_admin=is_admin)

    @app.context_processor
    def utility_processor():
        return dict(
            url_for_media_detail=url_for_media_detail,
            url_for_bookmark_create=url_for_bookmark_create,
            url_for_bookmark_remove=url_for_bookmark_remove
        )

def register_cache(app):
    app.cache = FileSystemCache(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'storage/cache'))

def register_route(app):
    from .routes import index, settings, media, bookmark, developer, oauth, dropbox, people
    from .routes import admin, api

    app.register_blueprint(admin.account.blueprint, url_prefix='/admin/account')
    app.register_blueprint(admin.list_media.blueprint, url_prefix='/admin/list-media')
    app.register_blueprint(admin.list_tweet.blueprint, url_prefix='/admin/list-tweet')
    app.register_blueprint(admin.list_user.blueprint, url_prefix='/admin/list-user')
    app.register_blueprint(admin.main.blueprint, url_prefix='/admin')
    app.register_blueprint(api.media.blueprint, url_prefix='/api/media')
    app.register_blueprint(api.main.blueprint, url_prefix='/api')
    app.register_blueprint(people.blueprint, url_prefix='/people')
    app.register_blueprint(dropbox.blueprint, url_prefix='/dropbox')
    app.register_blueprint(oauth.blueprint, url_prefix='/oauth')
    app.register_blueprint(developer.blueprint, url_prefix='/developer')
    app.register_blueprint(bookmark.blueprint, url_prefix='/bookmark')
    app.register_blueprint(media.blueprint, url_prefix='/media')
    app.register_blueprint(settings.blueprint, url_prefix='/settings')
    app.register_blueprint(index.blueprint, url_prefix='')
