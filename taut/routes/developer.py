import hmac
import base64
import hashlib
from flask import Blueprint, g, current_app
from flask import render_template, request, redirect, url_for, flash
from ..models import Developer
from ..helpers.account import require_user

blueprint = Blueprint('developer', __name__)

@blueprint.route('/')
@require_user
def index():
    return render_template('developer/index.html')

@blueprint.route('/request-api-key')
@require_user
def request_api_key():
    developer = Developer.query.filter_by(account_id=g.user.id).first()

    if developer:
        flash('You already has api key', 'error')
    else:
        digest    = hmac.new(
            current_app.config.get('API_SECRET_KEY'),
            msg = "{0}|{1}".format(g.user.username, g.user.create_at),
            digestmod = hashlib.sha256
        ).digest()
        signature = base64.b64encode(digest)

        Developer(
            account_id = g.user.id,
            api_key = signature
        ).save()

        flash('API key generated', 'success')

    return redirect(url_for('developer.index'))
