from flask import Blueprint, g
from flask import render_template, request
from ..models import ListUser
from ..helpers.value import force_integer

blueprint = Blueprint('people', __name__)

@blueprint.route('/index')
def index():
    page       = force_integer(request.args.get('page', 1), 0)
    list_users = ListUser.query.order_by(ListUser.create_at.desc()).paginate(page, 18)

    return render_template('people/index.html', list_users=list_users)
