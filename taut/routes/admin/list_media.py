from flask import Blueprint
from flask import render_template, request, abort, flash, redirect, url_for, jsonify
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
        return render_template('admin/list_media/index.html', status=status)

@blueprint.route('/ajax/index')
@require_admin
def ajax_index():
    status = request.args.get('status', 'hide')

    if status not in ['hide', 'show', 'trash']:
        return abort(403)
    else:
        page        = force_integer(request.args.get('page', 1), 0)
        next_url    = request.url

        if status == "hide":
            list_medias = ListMedia.query.filter_by(status=status).order_by(ListMedia.create_at.desc()).paginate(page)
        else:
            list_medias = ListMedia.query.filter_by(status=status).order_by(ListMedia.update_at.desc()).paginate(page)

        list_medias.items = fill_with_list_users(list_medias.items)

        prev_page = url_for('admin_list_media.ajax_index', page=page-1, _external=True) if list_medias.has_prev else None
        next_age  = url_for('admin_list_media.ajax_index', page=page+1, _external=True) if list_medias.has_next else None

    return jsonify(
        medias = [media.to_admin_json(media.user) for media in list_medias.items],
        prev   = prev_page,
        next   = next_age,
        count  = list_medias.total
    )

@blueprint.route('/ajax/status-control')
@require_admin
def ajax_status_control():
    media_id = force_integer(request.args.get('id', 0), 0)
    status   = request.args.get('status', 'hide')

    if status not in ['hide', 'show', 'trash']:
        return abort(403)
    else:
        media = ListMedia.query.get(media_id)
        media.status = status
        media.save()

        if media:
            return jsonify(status='success', message='Status changed');
        else:
            return jsonify(status='failed', message='Can not found media record');

@blueprint.route('/ajax/trash-all')
@require_admin
def ajax_trash_all():
    media_ids = request.args.getlist('ids[]')

    medias = ListMedia.query.filter(ListMedia.id.in_(media_ids)).all()

    for media in medias:
        media.status = 'trash'
        media.save()

    return jsonify(status='success', message='Trashed all')
