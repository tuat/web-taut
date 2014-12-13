# coding: utf-8

import hmac
import base64
import hashlib
from datetime import datetime
from ..models import ListUser

def force_integer(value, default=1):
    try:
        return int(value)
    except:
        return default

def fill_with_list_users(items):
    user_ids  = [item.list_user_id for item in items]
    users     = ListUser.query.filter(ListUser.id.in_(user_ids)).all() if user_ids else {}
    user_dict = {user.id: user for user in users}

    for item in items:
        item.user = user_dict.get(item.list_user_id)

    return items

def create_api_key(secret_key, user):
    digest = hmac.new(
        secret_key,
        msg = "{0}|{1}|{2}".format(user.username, user.create_at, datetime.now()),
        digestmod = hashlib.sha256
    ).digest()

    return base64.urlsafe_b64encode(digest)
