from flask import Blueprint, g
from flask import render_template, redirect, url_for
from ...forms import SigninForm
from ...models import ListUser, ListTweet, ListMedia, Account
from ...helpers.account import login_user, require_admin, logout_user

blueprint = Blueprint('admin_main', __name__)

@blueprint.route('/', methods=['GET', 'POST'])
def index():
    if g.user:
        return redirect(url_for('admin_main.home'))
    else:
        form = SigninForm()

        if form.validate_on_submit():
            login_user(form.user, form.permanent.data)
            return redirect(url_for('admin_main.home'))
        else:
            return render_template('admin/main/index.html', form=form)

@blueprint.route('/home')
@require_admin
def home():
    counter = dict(
        list_users  = ListUser.query.count(),
        list_tweets = ListTweet.query.count(),
        list_medias = dict(
            show = ListMedia.query.filter_by(status='show').count(),
            hide = ListMedia.query.filter_by(status='hide').count(),
            trash = ListMedia.query.filter_by(status='trash').count(),
            lost = ListMedia.query.filter_by(status='lost').count(),
        ),
        accounts    = Account.query.count()
    )

    return render_template('admin/main/home.html', counter=counter)

@blueprint.route('/logout')
@require_admin
def logout():
    logout_user()
    return redirect(url_for('admin_main.index'))
