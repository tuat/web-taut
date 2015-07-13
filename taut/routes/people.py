from flask import Blueprint, g
from flask import render_template, request, current_app
from ..models import ListUser, ListTweet, ListMedia, db
from ..helpers.value import force_integer, fill_with_list_users
from ..helpers.account import is_role

blueprint = Blueprint('people', __name__)

@blueprint.route('/index')
def index():
    if is_role('admin'):
        page       = force_integer(request.args.get('page', 1), 0)
        list_users = ListUser.query.order_by(ListUser.create_at.desc()).paginate(page, 15)
    else:
        list_users = current_app.cache.get('people_index_list_users')

        if list_users is None:
            list_users = ListUser.query.order_by(db.func.random()).offset(0).limit(18).all()

            current_app.cache.set('people_index_list_users', list_users, timeout=5*60)

    return render_template('people/index.html', list_users=list_users)

@blueprint.route('/profile/<screen_name>')
def profile(screen_name):
    list_user   = ListUser.query.filter(ListUser.screen_name == screen_name).first_or_404()
    list_tweets = ListTweet.query.filter(ListTweet.list_user_id == list_user.id).order_by(ListTweet.create_at.desc()).offset(0).limit(8).all()

    if is_role('admin'):
        page        = force_integer(request.args.get('page', 1), 0)
        list_medias = ListMedia.query.filter(
            ListMedia.list_user_id == list_user.id,
            ListMedia.status == 'show'
        ).order_by(ListMedia.create_at.desc()).paginate(page, 24)

        list_medias.items = fill_with_list_users(list_medias.items)
    else:
        list_medias = ListMedia.query.filter(
            ListMedia.list_user_id == list_user.id,
            ListMedia.status == 'show'
        ).order_by(ListMedia.create_at.desc()).offset(0).limit(24).all()
        list_medias = fill_with_list_users(list_medias)

    return render_template('people/profile.html', list_user=list_user, list_tweets=list_tweets, list_medias=list_medias)
