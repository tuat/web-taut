from flask import Blueprint, g
from flask import redirect, flash
from ..models import ListMedia, AccountConnection
from ..helpers.account import require_user
from ..helpers.value import url_for_media_detail, fill_with_list_users
from ..tasks.dropbox import sync_media_image

blueprint = Blueprint('dropbox', __name__)

@blueprint.route('/create/<list_media_id>')
@require_user
def create(list_media_id):
    media              = ListMedia.query.get_or_404(list_media_id)
    media              = fill_with_list_users([media])[0]
    account_connection = AccountConnection.query.filter_by(user_id=g.user.id, provider_name='dropbox').first()

    if not account_connection:
        flash('Please enable dropbox connection in your account settings page', 'error')
    else:
        sync_media_image.apply_async((g.user.id, media.id, media.user.screen_name))

        flash('Image is sending to your dropbox, Please check again after a while', 'success')

    return redirect(url_for_media_detail(media))
