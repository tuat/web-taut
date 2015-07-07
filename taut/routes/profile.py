from flask import Blueprint, g
from flask import render_template
from ..models import ListUser, ListTweet, ListMedia
from ..helpers.value import fill_with_list_users

blueprint = Blueprint('profile', __name__)

@blueprint.route('/<screen_name>')
def index(screen_name):
    list_user   = ListUser.query.filter(ListUser.screen_name == screen_name).first_or_404()
    list_tweets = ListTweet.query.filter(ListTweet.list_user_id == list_user.id).order_by(ListTweet.create_at.desc()).offset(0).limit(8).all()

    list_medias = ListMedia.query.filter(
        ListMedia.list_user_id == list_user.id,
        ListMedia.status == 'show'
    ).order_by(ListMedia.create_at.desc()).offset(0).limit(24).all()
    list_medias = fill_with_list_users(list_medias)

    return render_template('profile/index.html', list_user=list_user, list_tweets=list_tweets, list_medias=list_medias)
