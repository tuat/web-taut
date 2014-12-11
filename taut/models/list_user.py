# coding: utf-8

from datetime import datetime
from .base import SessionMixin, db

class ListUser(db.Model, SessionMixin):
    id                = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id           = db.Column(db.Integer, index=True)
    screen_name       = db.Column(db.String(120))
    profile_image_url = db.Column(db.String(180))
    last_tweet_id     = db.Column(db.String(30))
    create_at         = db.Column(db.DateTime, default=datetime.utcnow)
    update_at         = db.Column(db.DateTime, onupdate=datetime.utcnow)

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

    def __str__(self):
        return self.screen_name or self.user_id

    def __repr__(self):
        return '<ListUser: %s>' % self.id
