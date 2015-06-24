from flask import Blueprint
from flask import render_template, request, redirect, url_for
from ...models import ListUser
from ...helpers.account import require_admin
from ...helpers.value import force_integer

blueprint = Blueprint('admin_list_user', __name__)

@blueprint.route('/index')
@require_admin
def index():
    page        = force_integer(request.args.get('page', 1), 0)
    screen_name = request.args.get('screen_name')

    query = ListUser.query
    query = query.filter_by(screen_name=screen_name) if screen_name else query

    list_users  = query.order_by(ListUser.create_at.desc()).paginate(page)
    screen_name = screen_name if screen_name else ""

    return render_template('admin/list_user/index.html', list_users=list_users, screen_name=screen_name)

@blueprint.route('/search', methods=['POST'])
@require_admin
def search():
    screen_name = request.form['screen_name']

    return redirect(url_for('admin_list_user.index', screen_name=screen_name))
