# coding: utf-8

import hmac
import base64
import hashlib
from datetime import datetime
from hashids import Hashids
from flask import current_app, url_for

def force_integer(value, default=1):
    try:
        return int(value)
    except:
        return default

def fill_with_list_medias(items):
    from ..models import ListMedia

    media_ids  = [item.list_media_id for item in items]
    medias     = ListMedia.query.filter(ListMedia.id.in_(media_ids)).all() if media_ids else {}
    media_dict = {media.id: media for media in medias}

    for item in items:
        item.media = media_dict.get(item.list_media_id)

    return items

def fill_with_list_users(items):
    from ..models import ListUser

    user_ids  = [item.list_user_id for item in items]
    users     = ListUser.query.filter(ListUser.id.in_(user_ids)).all() if user_ids else {}
    user_dict = {user.id: user for user in users}

    for item in items:
        item.user = user_dict.get(item.list_user_id)

    return items

def fill_with_list_tweets(items):
    from ..models import ListTweet

    tweet_ids = [item.list_tweet_id for item in items]
    tweets    = ListTweet.query.filter(ListTweet.id.in_(tweet_ids)).all() if tweet_ids else {}
    tweet_dic = {tweet.id: tweet for tweet in tweets}

    for item in items:
        item.tweet = tweet_dic.get(item.list_tweet_id)

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
    if current_app.config['USE_ORIGNAL_IMAGE_URL']:
        url = url.replace("http://","")
    else:
        url = url.replace("http://pbs.twimg.com/media/","")

    url_parts = "{0}x{1}/{2}".format(width, height, url)

    if unsafe:
        return "{0}/unsafe/{1}".format(current_app.config.get('THUMBOR_BASE_URL'), url_parts)
    else:
        sign_code = base64.urlsafe_b64encode(hmac.new(current_app.config.get('THUMBOR_SECURITY_KEY'), url_parts, hashlib.sha1).digest())

        return "{0}/{1}/{2}".format(current_app.config.get('THUMBOR_BASE_URL'), sign_code, url_parts)

def human_time(value):
    now = datetime.utcnow()
    delta = now - value

    if delta.days > 365:
        return '{0} years ago'.format(delta.days / 365)
    if delta.days > 30:
        return '{0} months ago'.format(delta.days / 30)
    if delta.days > 0:
        return '{0} days ago'.format(delta.days)
    if delta.seconds > 3600:
        return '{0} hours ago'.format(delta.seconds / 3600)
    if delta.seconds > 60:
        return '{0} minutes ago'.format(delta.seconds / 60)

    return 'just now'

def create_media_hash_id(media):
    hash_salt = current_app.config['MEDIA_HASH_ID_SALT'] if current_app.config['MEDIA_HASH_ID_SALT'] else ""
    hash_ids  = Hashids(salt=hash_salt)

    return hash_ids.encode(media.id)

def url_for_media_detail(media, **kwargs):
    if current_app.config['USE_MEDIA_DETAIL_HASH_ID_IN_URL']:
        return url_for('media.detail', list_media_id=media.hash_id, **kwargs)
    else:
        return url_for('media.detail', list_media_id=media.id, **kwargs)
