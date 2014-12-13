from flask import Blueprint
from flask import render_template, redirect, url_for
from ..models import ListMedia, ListUser
from ..helpers.value import fill_with_users

blueprint = Blueprint('media', __name__)

@blueprint.route('/detail/<list_media_id>')
def detail(list_media_id):
    list_media  = ListMedia.query.get_or_404(list_media_id)
    list_user   = ListUser.query.get_or_404(list_media.list_user_id)
    user_medias = ListMedia.query.filter_by(list_user_id=list_media.list_user_id, status='show').order_by(ListMedia.create_at.desc()).offset(0).limit(12).all()
    user_medias = fill_with_users(user_medias)

    return render_template('media/detail.html', list_media=list_media, list_user=list_user, user_medias=user_medias)
