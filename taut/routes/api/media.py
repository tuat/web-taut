from flask import Blueprint
from flask import request, url_for, jsonify
from ...models import ListMedia, ListUser, ListTweet, Comment
from ...helpers.value import force_integer, fill_with_list_users, fill_with_accounts
from ...helpers.api import require_token, json_error

blueprint = Blueprint('api_media', __name__)

@blueprint.route('/detail/<list_media_id>', methods=['GET', 'POST'])
@require_token
def index(list_media_id):
    list_media = ListMedia.query.get(list_media_id)
    list_user  = ListUser.query.get(list_media.list_user_id)
    list_tweet = ListTweet.query.filter_by(id=list_media.list_tweet_id).first()

    user_medias = ListMedia.query.filter_by(list_user_id=list_media.list_user_id, status='show').order_by(ListMedia.create_at.desc()).offset(0).limit(12).all()
    user_medias = fill_with_list_users(user_medias)

    comments = Comment.query.filter_by(list_media_id=list_media_id).order_by(Comment.create_at.asc()).all()
    comments = fill_with_accounts(comments)

    return jsonify(
        image    = list_media.to_json(list_user, list_tweet),
        medias   = [media.to_json(list_user, list_tweet) for media in user_medias],
        comments = [comment.to_json() for comment in comments]
    )
