from flask import Blueprint
from flask import render_template, request, redirect, url_for, flash, abort
from ...models import Account
from ...helpers.account import require_admin
from ...helpers.value import force_integer

blueprint = Blueprint('admin_account', __name__)

@blueprint.route('/index')
@require_admin
def index():
    page     = force_integer(request.args.get('page', 1), 0)
    accounts = Account.query.order_by(Account.create_at.desc()).paginate(page)

    return render_template('admin/account/index.html', accounts=accounts)

@blueprint.route('/role/<account_id>/<role>')
@require_admin
def role(account_id, role):
    if role not in ['user', 'admin']:
        flash('Invalid role name', 'error')
    else:
        account = Account.query.get(account_id)
        account.role = role
        account.save()

        flash('Set the role success', 'success')

    return redirect(url_for('admin_account.index'))
