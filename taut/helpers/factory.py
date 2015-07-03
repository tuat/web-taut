import os
import rollbar
import rollbar.contrib.flask
from werkzeug.contrib.cache import FileSystemCache
from flask import g, got_request_exception
from flask.ext.babel import Babel, format_datetime
from flask.ext.assets import Environment
from flask.ext.oauthlib.client import OAuth
from ..models import db
from ..routes import index, settings, media, bookmark, developer, oauth, sync_dropbox
from ..routes import admin, api
from .helpers.account import load_current_user
from .helpers.value import thumb, human_time, url_for_media_detail

def register_flask_hook(app):
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

def register_flask_babel(app):
    babel = Babel(app)

def register_flask_assets(app):
    assets = Environment()
    assets.init_app(app)

def register_flask_oauth(app):
    oauth   = OAuth(app)
    dropbox = oauth.remote_app('dropbox', app_key='DROPBOX')

    app.oauth = oauth
    app.oauth.providers = {
        'dropbox': dropbox
    }

def register_flask_jinja2(app):
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

def register_flask_database(app):
    db.init_app(app)
    db.app = app

def register_flask_cache(app):
    app.cache = FileSystemCache(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'storage/random_medias'))

def register_flask_route(app):
    app.register_blueprint(admin.account.blueprint, url_prefix='/admin/account')
    app.register_blueprint(admin.list_media.blueprint, url_prefix='/admin/list-media')
    app.register_blueprint(admin.list_tweet.blueprint, url_prefix='/admin/list-tweet')
    app.register_blueprint(admin.list_user.blueprint, url_prefix='/admin/list-user')
    app.register_blueprint(admin.main.blueprint, url_prefix='/admin')
    app.register_blueprint(api.media.blueprint, url_prefix='/api/media')
    app.register_blueprint(api.main.blueprint, url_prefix='/api')
    app.register_blueprint(sync_dropbox.blueprint, url_prefix='/dropbox')
    app.register_blueprint(oauth.blueprint, url_prefix='/oauth')
    app.register_blueprint(developer.blueprint, url_prefix='/developer')
    app.register_blueprint(bookmark.blueprint, url_prefix='/bookmark')
    app.register_blueprint(media.blueprint, url_prefix='/media')
    app.register_blueprint(settings.blueprint, url_prefix='/settings')
    app.register_blueprint(index.blueprint, url_prefix='')
