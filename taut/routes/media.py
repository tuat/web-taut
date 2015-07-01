from flask import Blueprint, g
from flask import render_template, redirect, url_for, flash
from ..models import ListMedia, ListTweet, ListUser, Comment, db
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
            list_media = ListMedia.query.filter(
                db.or_(
                    ListMedia.id == list_media_id,
                    ListMedia.hash_id == list_media_id
                )
            ).first_or_404()

            comment = form.save(list_media.id, g.user)
            flash('Your comment created', 'success')

            return redirect("{0}#comment-{1}".format(url_for('media.detail', list_media_id=list_media_id), comment.id))

        return save_form()
    else:
        list_media = ListMedia.query.filter(
            db.or_(
                ListMedia.id == list_media_id,
                ListMedia.hash_id == list_media_id
            )
        ).first_or_404()

        list_user  = ListUser.query.get_or_404(list_media.list_user_id)
        list_tweet = ListTweet.query.filter_by(id=list_media.list_tweet_id).first()

        user_medias = ListMedia.query.filter_by(list_user_id=list_media.list_user_id, status='show').order_by(ListMedia.create_at.desc()).offset(0).limit(12).all()
        user_medias = fill_with_list_users(user_medias)

        random_medias = ListMedia.query.filter_by(status='show').order_by(db.func.random()).offset(0).limit(20).all()[0:6]
        random_medias = fill_with_list_users(random_medias)

        comments = Comment.query.filter_by(list_media_id=list_media.id).order_by(Comment.create_at.asc()).all()
        comments = fill_with_accounts(comments)

        return render_template('media/detail.html', list_media=list_media, list_user=list_user, list_tweet=list_tweet, user_medias=user_medias, form=form, random_medias=random_medias, comments=comments)
