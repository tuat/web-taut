from flask import Blueprint, g
from flask import render_template, request, redirect, url_for, flash
from ..forms import ProfileForm, PasswordForm
from ..models import Account

blueprint = Blueprint('settings', __name__)

@blueprint.route('/profile', methods=['GET', 'POST'])
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
