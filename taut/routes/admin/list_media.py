from flask import Blueprint
from flask import render_template, request, abort
from ...models import ListMedia
from ...helpers.value import force_integer, fill_with_users

blueprint = Blueprint('admin_list_media', __name__)

@blueprint.route('/index/<status>')
def index(status):
    if status not in ['hide', 'show', 'trash']:
        return abort(403)
    else:
        page        = force_integer(request.args.get('page', 1), 0)
        list_medias = ListMedia.query.filter_by(status=status).order_by(ListMedia.create_at.desc()).paginate(page)

        list_medias.items = fill_with_users(list_medias.items)

        return render_template('admin/list_media/index.html', list_medias=list_medias, status=status)

@blueprint.route('/hide')
def hide():
    return "hide"

@blueprint.route('/show')
def show():
    return "show"

@blueprint.route('/trash')
def trash():
    return "trash"
