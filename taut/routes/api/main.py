from flask import Blueprint
from flask import render_template, request, url_for, jsonify
from ...models import ListMedia
from ...forms import SigninForm
from ...helpers.value import force_integer, fill_with_list_users, fill_with_list_tweets
from ...helpers.api import require_token, json_error
from ...helpers.account import logout_user, require_user, login_user

blueprint = Blueprint('api_main', __name__)

@blueprint.route('/')
@require_token
def index():
    """
    Get media list
    ---
    tags:
        - home
    parameters:
        - name: token
          in: query
          description: access token
          required: true
          type: string
        - name: page
          in: query
          description: number of page
          required: false
          type: number
          format: integer
    responses:
        200:
            description: An array of medias with paginate information
            schema:
                id: MediaesWithPaingate
                properties:
                    items:
                        description: the media objects
                        schema:
                            id: Media
                            properties:
                                id:
                                    type: string
                                    description: the id of media
                                media_url:
                                    type: string
                                    description: the image url of media
                                width:
                                    type: number
                                    format: integer
                                    description: the width of media
                                height:
                                    type: number
                                    format: integer
                                    description: the height of media
                                user:
                                    description: the user of media
                                    schema:
                                        id: User
                                        properties:
                                            id:
                                                type: number
                                                description: the id of media owner user
                                            name:
                                                type: string
                                                description: the name of media owner user
                                            screen_name:
                                                type: string
                                                description: the username of media owner user
                                tweet:
                                    description: the tweet of media
                                    schema:
                                        id: Tweet
                                        properties:
                                            text:
                                                type: string
                                                description: the tweet of media
                    prev:
                        type: number
                        description: number of previous page
                    next:
                        type: number
                        description: number of next page
                    count:
                        type: number
                        description: total number of medias

    """

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
