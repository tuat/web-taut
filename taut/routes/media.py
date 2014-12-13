from flask import Blueprint, g
from flask import render_template, redirect, url_for, flash
from ..models import ListMedia, ListUser, Comment
from ..forms import CommentForm
from ..helpers.value import fill_with_list_users, fill_with_accounts
from ..helpers.account import require_user

blueprint = Blueprint('media', __name__)

@blueprint.route('/detail/<list_media_id>', methods=['GET', 'POST'])
def detail(list_media_id):
    form = CommentForm()

    if form.validate_on_submit():
        @require_user
        def save_form():
            comment = form.save(list_media_id, g.user)
            flash('Your comment created', 'success')

            return redirect("{0}#comment-{1}".format(url_for('media.detail', list_media_id=list_media_id), comment.id))

        return save_form()
    else:
        list_media  = ListMedia.query.get_or_404(list_media_id)
        list_user   = ListUser.query.get_or_404(list_media.list_user_id)
        user_medias = ListMedia.query.filter_by(list_user_id=list_media.list_user_id, status='show').order_by(ListMedia.create_at.desc()).offset(0).limit(12).all()
        user_medias = fill_with_list_users(user_medias)

        comments = Comment.query.filter_by(list_media_id=list_media_id).order_by(Comment.create_at.asc()).all()
        comments = fill_with_accounts(comments)

        return render_template('media/detail.html', list_media=list_media, list_user=list_user, user_medias=user_medias, form=form, comments=comments)
