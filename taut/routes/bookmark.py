from flask import Blueprint, g
from flask import render_template, redirect, url_for, flash, request
from ..models import ListMedia, Bookmark
from ..helpers.account import require_user
from ..helpers.value import force_integer

blueprint = Blueprint('bookmark', __name__)

@blueprint.route('/index')
@require_user
def index():
    # Get bookmarks
    page        = force_integer(request.args.get('page', 1), 0)
    bookmarks   = Bookmark.query.filter_by(account_id=g.user.id).order_by(Bookmark.create_at.desc()).paginate(page)

    # Find all medias by bookmarks.list_media_id
    list_media_ids = [item.list_media_id for item in bookmarks.items]
    list_medias    = ListMedia.query.filter(ListMedia.id.in_(list_media_ids)).all()

    return render_template('bookmark/index.html', bookmarks=bookmarks, list_medias=list_medias)

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
