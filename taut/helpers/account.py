import functools
from flask import session, g, redirect, url_for, abort
from ..models import Account

def login_user(user, permanent=False):
    if not user:
        return None
    else:
        session['id'] = user.id

        if permanent:
            session.permanent = True

        return user

def load_current_user():
    if 'id' in session:
        user = Account.query.get(int(session['id']))

        if not user:
            return None
        else:
            return user
    else:
        return None

def require_role(role):
    def _require_role(method):
        @functools.wraps(method)
        def wrapper(*args, **kwargs):
            if not g.user:
                return redirect(url_for('admin_main.index'))
            if role is None:
                return method(*args, **kwargs)
            # if g.user.id == 1:
            #     return method(*args, **kwargs)
            if g.user.role != role:
                return abort(403)
            return method(*args, **kwargs)
        return wrapper
    return _require_role

require_admin = require_role('admin')
