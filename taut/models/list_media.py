# coding: utf-8

from datetime import datetime
from sqlalchemy.sql import exists
from sqlalchemy.ext.hybrid import hybrid_method
from flask import current_app
from .base import SessionMixin, db
from .bookmark import Bookmark
from ..helpers.value import thumb, proxy_media_url

class ListMedia(db.Model, SessionMixin):
    id            = db.Column(db.Integer, primary_key=True, autoincrement=True)
    list_user_id  = db.Column(db.Integer, index=True)
    list_tweet_id = db.Column(db.Integer, index=True)
    id_str        = db.Column(db.String(30)) # media id_str
    media_url     = db.Column(db.String(180))
    type          = db.Column(db.String(20))
    status        = db.Column(db.String(10), default="hide")
    hash_id       = db.Column(db.String(64))
    create_at     = db.Column(db.DateTime, default=datetime.utcnow)
    update_at     = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

    def __str__(self):
        return self.media_url

    def __repr__(self):
        return '<ListMedia: %s>' % self.id

    @property
    def is_hide(self):
        return self.status == "hide"

    @property
    def is_show(self):
        return self.status == "show"

    @property
    def is_trash(self):
        return self.status == "trash"

    @property
    def is_lost(self):
        return self.status == "lost"

    @hybrid_method
    def is_bookmarked(self, user):
        if user:
            return db.session.query(db.session.query(Bookmark).filter(
                Bookmark.list_media_id == self.id,
                Bookmark.account_id == user.id
            ).exists()).scalar()
        else:
            return False

    def to_json(self, list_user, list_tweet):
        width  = 500
        height = 500

        return {
            'id'       : self.hash_id if current_app.config.get('USE_MEDIA_DETAIL_HASH_ID_IN_URL') else self.hash_id,
            'media_url': proxy_media_url(self.media_url), # 'media_url': thumb(self.media_url, width, height),
            'width'    : width,
            'height'   : height,
            'user'     : list_user.to_json(),
            'tweet'    : list_tweet.to_json()
        }

    def to_admin_json(self, list_user):
        width  = 300
        height = 300

        return {
            'id'        : self.hash_id if current_app.config.get('USE_MEDIA_DETAIL_HASH_ID_IN_URL') else self.hash_id,
            'media_url' : self.media_url,
            'thumb_url' : thumb(self.media_url, width, height, fill_in_fit=True),
            'user'      : list_user.to_admin_json(),
            'is_hide'   : self.is_hide,
            'is_show'   : self.is_show,
            'is_trash'  : self.is_trash,
            'is_lost'   : self.is_lost
        }
