# coding: utf-8

from datetime import datetime
from .base import SessionMixin, db

class ListMedia(db.Model, SessionMixin):
    id            = db.Column(db.Integer, primary_key=True, autoincrement=True)
    list_user_id  = db.Column(db.Integer, index=True)
    list_tweet_id = db.Column(db.Integer, index=True)
    media_url     = db.Column(db.String(180))
    type          = db.Column(db.String(10))
    create_at     = db.Column(db.DateTime, default=datetime.utcnow)
    update_at     = db.Column(db.DateTime, onupdate=datetime.utcnow)

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

    def __str__(self):
        return self.media_url

    def __repr__(self):
        return '<ListMedia: %s>' % self.id
