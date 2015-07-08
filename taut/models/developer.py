# coding: utf-8

from .base import db, SessionMixin
from datetime import datetime

class Developer(db.Model, SessionMixin):
    id         = db.Column(db.Integer, primary_key=True, autoincrement=True)
    account_id = db.Column(db.Integer, index=True)
    api_key    = db.Column(db.String(120), index=True)
    create_at  = db.Column(db.DateTime, default=datetime.utcnow)
    update_at  = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

    def __str__(self):
        return self.id

    def __repr__(self):
        return '<Developer: %s>' % self.id
