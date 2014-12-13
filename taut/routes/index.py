from flask import Blueprint
from flask import render_template, request, redirect, url_for, flash
from ..models import ListMedia
from ..forms import SigninForm, SignupForm
from ..helpers.account import logout_user, login_user, require_user
from ..helpers.value import force_integer, fill_with_list_users

blueprint = Blueprint('index', __name__)

@blueprint.route('/')
def index():
    page        = force_integer(request.args.get('page', 1), 0)
    list_medias = ListMedia.query.filter_by(status='show').order_by(ListMedia.create_at.desc()).paginate(page)

    list_medias.items = fill_with_list_users(list_medias.items)

    return render_template('index.html', list_medias=list_medias)

@blueprint.route('/logout')
@require_user
def logout():
    logout_user()
    return redirect(url_for('index.index'))

@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = SigninForm()

    if form.validate_on_submit():
        login_user(form.user, form.permanent.data)
        return redirect(url_for('index.index'))
    else:
        return render_template('login.html', form=form)

@blueprint.route('/register', methods=['GET', 'POST'])
def register():
    form = SignupForm()

    if form.validate_on_submit():
        account = form.save()
        flash('Thanks for your register. Your account has been created', 'success')
        return redirect(url_for('index.signup'))

    return render_template('register.html', form=form)
