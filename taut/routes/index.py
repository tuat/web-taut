from flask import Blueprint
from flask import render_template, request
from ..models import ListMedia
from ..helpers.value import force_integer, fill_with_users

blueprint = Blueprint('index', __name__)

@blueprint.route('/')
def index():
    page        = force_integer(request.args.get('page', 1), 0)
    list_medias = ListMedia.query.filter_by(status='show').order_by(ListMedia.create_at.desc()).paginate(page)

    list_medias.items = fill_with_users(list_medias.items)

    return render_template('index.html', list_medias=list_medias)
