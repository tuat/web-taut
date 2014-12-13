from flask import Blueprint
from flask import render_template, request, abort, flash, redirect, url_for
from ...models import ListMedia
from ...helpers.account import require_admin
from ...helpers.value import force_integer, fill_with_list_users

blueprint = Blueprint('admin_list_media', __name__)

@blueprint.route('/index/<status>')
@require_admin
def index(status):
    if status not in ['hide', 'show', 'trash']:
        return abort(403)
    else:
        page        = force_integer(request.args.get('page', 1), 0)
        next_url    = request.url
        list_medias = ListMedia.query.filter_by(status=status).order_by(ListMedia.create_at.desc()).paginate(page)

        list_medias.items = fill_with_list_users(list_medias.items)

        return render_template('admin/list_media/index.html', list_medias=list_medias, status=status, next_url=next_url)

@blueprint.route('/hide/<int:list_media_id>')
@require_admin
def hide(list_media_id):
    next_url = request.args.get('next')

    list_media = ListMedia.query.get_or_404(list_media_id)
    list_media.status = "hide"
    list_media.save()

    flash('The media was marked as hide', 'success')

    return redirect(next_url)

@blueprint.route('/show/<int:list_media_id>')
@require_admin
def show(list_media_id):
    next_url = request.args.get('next')

    list_media = ListMedia.query.get_or_404(list_media_id)
    list_media.status = "show"
    list_media.save()

    flash('The media was marked as show', 'success')

    return redirect(next_url)

@blueprint.route('/trash/<int:list_media_id>')
@require_admin
def trash(list_media_id):
    next_url = request.args.get('next')

    list_media = ListMedia.query.get_or_404(list_media_id)
    list_media.status = "trash"
    list_media.save()

    flash('The media was marked as trash', 'success')

    return redirect(next_url)
