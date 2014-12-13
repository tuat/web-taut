# coding: utf-8

import hmac
import base64
import hashlib
from datetime import datetime
from flask import current_app

def force_integer(value, default=1):
    try:
        return int(value)
    except:
        return default

def fill_with_list_users(items):
    from ..models import ListUser

    user_ids  = [item.list_user_id for item in items]
    users     = ListUser.query.filter(ListUser.id.in_(user_ids)).all() if user_ids else {}
    user_dict = {user.id: user for user in users}

    for item in items:
        item.user = user_dict.get(item.list_user_id)

    return items

def fill_with_accounts(items):
    from ..models import Account

    account_ids  = [item.account_id for item in items]
    accounts     = Account.query.filter(Account.id.in_(account_ids)).all() if account_ids else {}
    account_dict = {account.id: account for account in accounts}

    for item in items:
        item.user = account_dict.get(item.account_id)

    return items

def create_api_key(secret_key, user):
    digest = hmac.new(
        secret_key,
        msg = "{0}|{1}|{2}".format(user.username, user.create_at, datetime.now()),
        digestmod = hashlib.sha256
    ).digest()

    return base64.urlsafe_b64encode(digest)

def thumb(url, width, height, unsafe=False):
    url_parts = "{0}x{1}/{2}".format(width, height, url.replace("http://",""))

    if unsafe:
        return "{0}/unsafe/{1}".format(current_app.config.get('THUMBOR_BASE_URL'), url_parts)
    else:
        sign_code = base64.urlsafe_b64encode(hmac.new(current_app.config.get('THUMBOR_SECURITY_KEY'), url_parts, hashlib.sha1).digest())

        return "{0}/{1}/{2}".format(current_app.config.get('THUMBOR_BASE_URL'), sign_code, url_parts)
