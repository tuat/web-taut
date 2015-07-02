import re
from flask import Blueprint, g
from flask import current_app, flash, redirect, url_for, session, request
from ..helpers.oauth import authorized_callback
from ..models import AccountConnection

blueprint = Blueprint('oauth', __name__)

@blueprint.route('/connect/<provider>', defaults={ 'kind': 'normal' })
@blueprint.route('/connect/<provider>/<kind>')
def connect(provider, kind):
    providers = current_app.oauth.providers

    if provider in providers:
        if provider == 'dropbox' and re.match(r'^localhost:\d+$', request.host) is None:
            return providers[provider].authorize(callback=url_for('oauth.authorized', provider=provider, kind=kind, _external=True, _scheme='https'))
        else:
            return providers[provider].authorize(callback=url_for('oauth.authorized', provider=provider, kind=kind, _external=True))
    else:
        flash('Not found provider', 'error')
        return redirect(url_for('index.signin'))

@blueprint.route('/disconnect/<provider>')
def disconnect(provider):
    providers = current_app.oauth.providers

    if provider in providers:
        session.pop('{0}_token'.format(provider.lower()), None)

        if g.user:
            user_connection = AccountConnection.query.filter_by(user_id=g.user.id, provider_name=provider).first()
            user_connection.access_token = ""
            user_connection.save()

            flash('Disconnect to {0} completed'.format(provider.capitalize()), 'success')

            return redirect(url_for('settings.connection'))
        else:
            return redirect(url_for('index.index'))
    else:
        flash('Not found provider', 'error')
        return redirect(url_for('index.login'))


    return redirect(url_for('index.index'))

@blueprint.route('/connect/authorized/<provider>', defaults={ 'kind': 'normal' })
@blueprint.route('/connect/authorized/<provider>/<kind>')
def authorized(provider, kind):
    providers = current_app.oauth.providers

    if provider in providers:
        return providers[provider].authorized_handler(authorized_callback)(provider, kind)
    else:
        flash('Not found provider', 'error')
        return redirect(url_for('user.login'))
