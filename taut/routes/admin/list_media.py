from flask import Blueprint
from flask import render_template, request, abort, flash, redirect, url_for, jsonify
from ...models import ListMedia
from ...helpers.account import require_admin
from ...helpers.value import force_integer, fill_with_list_users

blueprint = Blueprint('admin_list_media', __name__)

@blueprint.route('/index/<status>')
@require_admin
def index(status):
    if status not in ['hide', 'show', 'trash', 'lost']:
        return abort(403)
    else:
        return render_template('admin/list_media/index.html', status=status)

@blueprint.route('/search', methods=['GET', 'POST'])
@require_admin
def search():
    if request.method == 'POST':
        media_id = request.form['media_id']

        return redirect(url_for('admin_list_media.search', media_id=media_id))
    else:
        media_id = request.args.get('media_id')

        if media_id:
            media = ListMedia.query.filter(
                (ListMedia.id == media_id) |
                (ListMedia.hash_id == media_id) |
                (ListMedia.media_url.like("%{0}%".format(media_id)))
            ).first()

            media = fill_with_list_users([media])[0]
        else:
            media_id = ""
            media    = ""

        return render_template('admin/list_media/search.html', media_id=media_id, media=media)

@blueprint.route('/ajax/index')
@require_admin
def ajax_index():
    status = request.args.get('status', 'hide')

    if status not in ['hide', 'show', 'trash', 'lost']:
        return abort(403)
    else:
        page        = force_integer(request.args.get('page', 1), 0)
        next_url    = request.url

        list_medias = ListMedia.query.filter_by(status=status).order_by(ListMedia.update_at.desc()).paginate(page, 100)

        list_medias.items = fill_with_list_users(list_medias.items)

        prev_page  = url_for('admin_list_media.ajax_index', page=page-1) if list_medias.has_prev else None
        next_page  = url_for('admin_list_media.ajax_index', page=page+1) if list_medias.has_next else None

        return jsonify(
            medias = [media.to_admin_json(media.user) for media in list_medias.items],
            prev   = prev_page,
            next   = next_page,
            count  = list_medias.total
        )

@blueprint.route('/ajax/status-control')
@require_admin
def ajax_status_control():
    media_id = force_integer(request.args.get('id', 0), 0)
    status   = request.args.get('status', 'hide')

    if status not in ['hide', 'show', 'trash', 'lost']:
        return abort(403)
    else:
        media = ListMedia.query.get(media_id)
        media.status = status
        media.save()

        if media:
            return jsonify(status='success', message='Status changed');
        else:
            return jsonify(status='failed', message='Can not found media record');

@blueprint.route('/ajax/trash-all', methods=['POST'])
@require_admin
def ajax_trash_all():
    media_ids = request.form.getlist('ids[]')

    medias = ListMedia.query.filter(ListMedia.id.in_(media_ids)).all()

    for media in medias:
        media.status = 'trash'
        media.save()

    return jsonify(status='success', message='Trashed all')

