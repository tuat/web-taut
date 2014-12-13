from flask import Blueprint, g
from flask import render_template, redirect, url_for, flash
from ..models import ListMedia, Bookmark
from ..helpers.account import require_user

blueprint = Blueprint('bookmark', __name__)

@blueprint.route('/create/<list_media_id>')
@require_user
def create(list_media_id):
    list_media = ListMedia.query.get_or_404(list_media_id)
    bookmark   = Bookmark.query.filter_by(list_media_id=list_media_id, account_id=g.user.id).first()

    if bookmark:
        flash('The media already bookmarked', 'error')
    else:
        Bookmark(
            list_media_id = list_media_id,
            account_id    = g.user.id
        ).save()

        flash('The media was bookmarked', 'success')

    return redirect(url_for('media.detail', list_media_id=list_media_id))

@blueprint.route('/remove/<list_media_id>')
@require_user
def remove(list_media_id):
    list_media = ListMedia.query.get_or_404(list_media_id)
    bookmark   = Bookmark.query.filter_by(list_media_id=list_media_id, account_id=g.user.id).first()

    if not bookmark:
        flash('You are not created bookmark on this media', 'error')
    else:
        bookmark.delete()

        flash('The media was removed from bookmark', 'success')

    return redirect(url_for('media.detail', list_media_id=list_media_id))
