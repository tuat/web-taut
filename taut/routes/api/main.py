from flask import Blueprint
from flask import render_template, request, url_for, jsonify
from ...models import ListMedia
from ...helpers.value import force_integer, fill_with_list_users, fill_with_list_tweets
from ...helpers.api import require_token, json_error
from ...helpers.account import logout_user, require_user

blueprint = Blueprint('api_main', __name__)

@blueprint.route('/')
@require_token
def index():
    page        = force_integer(request.args.get('page', 1), 0)
    list_medias = ListMedia.query.filter_by(status='show').order_by(ListMedia.create_at.desc()).paginate(page)

    list_medias.items = fill_with_list_users(list_medias.items)
    list_medias.items = fill_with_list_tweets(list_medias.items)

    prev_page = url_for('api_main.index', page=page-1, _external=True) if list_medias.has_prev else None
    next_age  = url_for('api_main.index', page=page+1, _external=True) if list_medias.has_next else None

    return jsonify(
        items = [media.to_json(media.user, media.tweet) for media in list_medias.items],
        prev  = prev_page,
        next  = next_age,
        count = list_medias.total
    )

@blueprint.route('/logout')
@require_token
@require_user
def logout():
    logout_user()
    return jsonify(
        status = 200
    )
