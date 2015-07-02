from flask import Blueprint, g
from flask import render_template, request, redirect, url_for, flash
from ..forms import ProfileForm, PasswordForm
from ..models import Account, AccountConnection
from ..helpers.account import require_user

blueprint = Blueprint('settings', __name__)

@blueprint.route('/profile', methods=['GET', 'POST'])
@require_user
def profile():
    form = ProfileForm(obj=g.user)

    if g.user.username != form.username.data and form.validate_on_submit():
        user = Account.query.get(g.user.id)
        form.populate_obj(user)
        user.save()

        flash('Your profile was updated', 'success')

        return redirect(url_for('settings.profile'))
    else:
        return render_template('settings/profile.html', form=form)

@blueprint.route('/password', methods=['GET', 'POST'])
@require_user
def password():
    form = PasswordForm(obj=g.user)

    if form.validate_on_submit():
        user = Account.query.get(g.user.id)
        user.update_password(form.new_password.data)
        form.populate_obj(user)
        user.save()

        flash('Your password was updated, Please sign in again', 'success')

        return redirect(url_for('index.logout'))
    else:
        return render_template('settings/password.html', form=form)

@blueprint.route('/connection', methods=['GET', 'POST'])
@require_user
def connection():
    account_connections = AccountConnection.query.filter(
        AccountConnection.user_id == g.user.id,
        AccountConnection.access_token != ''
    ).all()

    connected_providers = [account_connection.provider_name for account_connection in account_connections]

    return render_template('settings/connection.html', connected_providers=connected_providers)
