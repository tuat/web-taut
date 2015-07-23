from flask import Blueprint, current_app
from flask import render_template, request, abort, flash, redirect, url_for, jsonify
from ...models import ListMedia
from ...helpers.account import require_admin
from ...helpers.value import force_integer, fill_with_list_users, get_media_hash_id_where_sql

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
        keyword = request.form['keyword']
        type    = request.form['type']

        return redirect(url_for('admin_list_media.search', keyword=keyword, type=type))
    else:
        keyword = request.args.get('keyword')
        type    = request.args.get('type')

        if keyword and type:
            media = ListMedia.query
            media = media.filter(ListMedia.id == force_integer(keyword, 0)) if type == "media-id" else media
            media = media.filter(ListMedia.hash_id == keyword) if type == "hash-id" else media
            media = media.filter(ListMedia.media_url.like("%{0}%".format(keyword))) if type == "photo-file-name" else media
            media = media.first()

            if media:
                media = fill_with_list_users([media])[0]
        else:
            keyword = ""
            media   = ""

        return render_template('admin/list_media/search.html', keyword=keyword, type=type, media=media)

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
            medias      = [media.to_admin_json(media.user) for media in list_medias.items],
            prev        = prev_page,
            next        = next_page,
            count       = list_medias.total,
        )

@blueprint.route('/ajax/status-control')
@require_admin
def ajax_status_control():
    media_id = request.args.get('id', "")
    status   = request.args.get('status', 'hide')

    if status not in ['hide', 'show', 'trash', 'lost']:
        return abort(403)
    else:
        where_sql = get_media_hash_id_where_sql(media_id)

        media = ListMedia.query.filter(where_sql).first_or_404()
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

    where_sql = get_media_hash_id_where_sql(media_ids)
    medias    = ListMedia.query.filter(where_sql).all()

    for media in medias:
        media.status = 'trash'
        media.save()

    return jsonify(status='success', message='Trashed all')

