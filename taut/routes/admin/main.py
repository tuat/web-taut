from flask import Blueprint
from flask import render_template, redirect, url_for
from ...forms import SigninForm
from ...helpers.account import login_user, require_admin, logout_user

blueprint = Blueprint('admin_main', __name__)

@blueprint.route('/', methods=['GET', 'POST'])
def index():
    form = SigninForm()

    if form.validate_on_submit():
        login_user(form.user, form.permanent.data)
        return redirect(url_for('admin_main.home'))
    else:
        return render_template('admin/main/index.html', form=form)

@blueprint.route('/home')
@require_admin
def home():
    return render_template('admin/main/home.html')

@blueprint.route('/logout')
@require_admin
def logout():
    logout_user()
    return redirect(url_for('admin_main.index'))
