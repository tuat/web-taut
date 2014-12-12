from flask import Blueprint
from flask import render_template, request
from ...models import ListUser
from ...helpers.account import require_admin
from ...helpers.value import force_integer

blueprint = Blueprint('admin_list_user', __name__)

@blueprint.route('/index')
@require_admin
def index():
    page       = force_integer(request.args.get('page', 1), 0)
    list_users = ListUser.query.order_by(ListUser.create_at.desc()).paginate(page)

    return render_template('admin/list_user/index.html', list_users=list_users)
