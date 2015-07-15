from flask import Blueprint, g
from flask import render_template, redirect, url_for, flash, request
from ..models import ListMedia, Bookmark, ListUser, Account
from ..helpers.account import require_user
from ..helpers.value import force_integer, fill_with_list_users

blueprint = Blueprint('bookmark', __name__)

@blueprint.route('/index')
@require_user
def index():
    page        = force_integer(request.args.get('page', 1), 0)
    screen_name = request.args.get('screen_name')

    # Get bookmarks
    if screen_name:
        list_user      = ListUser.query.filter(ListUser.screen_name == screen_name).first_or_404()
        list_media_ids = ListMedia.query.with_entities(ListMedia.id).filter(ListMedia.list_user_id == list_user.id).subquery()
        bookmarks      = Bookmark.query.filter(Bookmark.account_id == g.user.id, Bookmark.list_media_id.in_(list_media_ids)).paginate(page)
    else:
        bookmarks      = Bookmark.query.filter_by(account_id=g.user.id).order_by(Bookmark.create_at.desc()).paginate(page)

    # Create list media ids by bookmarked records
    list_media_ids = [item.list_media_id for item in bookmarks.items]

    # Find all medias by bookmarks.list_media_id
    list_medias = ListMedia.query.filter(ListMedia.id.in_(list_media_ids)).all()
    list_medias = fill_with_list_users(list_medias)

    # Find bookmkared user from current bookmkared list
    bookmarked_list  = Bookmark.query.filter_by(account_id=g.user.id).order_by(Bookmark.create_at.desc()).all()
    bookmarked_ids   = [bookmarked.list_media_id for bookmarked in bookmarked_list]
    distanct_medias  = ListMedia.query.distinct(ListMedia.list_user_id).filter(ListMedia.id.in_(bookmarked_ids)).all()
    distanct_users   = [media.list_user_id for media in distanct_medias]
    bookmarked_users = ListUser.query.filter(ListUser.id.in_(distanct_users)).all()

    return render_template('bookmark/index.html', page=page, screen_name=screen_name, bookmarks=bookmarks, list_medias=list_medias, bookmarked_users=bookmarked_users)

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
