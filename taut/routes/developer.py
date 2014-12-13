from flask import Blueprint, g, current_app
from flask import render_template, request, redirect, url_for, flash
from ..models import Developer
from ..helpers.account import require_user
from ..helpers.value import create_api_key

blueprint = Blueprint('developer', __name__)

@blueprint.route('/')
@require_user
def index():
    developer = Developer.query.filter_by(account_id=g.user.id).first()

    return render_template('developer/index.html', developer=developer)

@blueprint.route('/request-api-key')
@require_user
def request_api_key():
    developer = Developer.query.filter_by(account_id=g.user.id).first()

    if developer:
        flash('You already has api key', 'error')
    else:
        Developer(
            account_id = g.user.id,
            api_key = create_api_key(current_app.config.get('API_SECRET_KEY'), g.user)
        ).save()

        flash('API key generated', 'success')

    return redirect(url_for('developer.index'))

@blueprint.route('/renew_api_key')
def renew_api_key():
    developer = Developer.query.filter_by(account_id=g.user.id).first()

    if not developer:
        flash('Please request api key first', 'error')
    else:
        developer.api_key = create_api_key(current_app.config.get('API_SECRET_KEY'), g.user)
        developer.save()

        flash('API key re-generated', 'success')

    return redirect(url_for('developer.index'))
