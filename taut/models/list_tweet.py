# coding: utf-8

from datetime import datetime
from .base import SessionMixin, db

class ListTweet(db.Model, SessionMixin):
    id           = db.Column(db.Integer, primary_key=True, autoincrement=True)
    list_user_id = db.Column(db.Integer, index=True)
    id_str       = db.Column(db.String(30), index=True) # tweet id_str
    text         = db.Column(db.Text)
    create_at    = db.Column(db.DateTime, default=datetime.utcnow)
    update_at    = db.Column(db.DateTime, onupdate=datetime.utcnow)

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

    def __str__(self):
        return self.text

    def __repr__(self):
        return '<ListTweet: %s>' % self.id
