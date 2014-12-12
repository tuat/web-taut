# coding: utf-8

from ..models import ListUser

def force_integer(value, default=1):
    try:
        return int(value)
    except:
        return default

def fill_with_users(items):
    user_ids  = [item.list_user_id for item in items]
    users     = ListUser.query.filter(ListUser.id.in_(user_ids)).all() if user_ids else {}
    user_dict = {user.id: user for user in users}

    for item in items:
        item.user = user_dict.get(item.list_user_id)

    return items
