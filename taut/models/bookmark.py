# coding: utf-8

from .base import db, SessionMixin
from datetime import datetime

class Bookmark(db.Model, SessionMixin):
    id            = db.Column(db.Integer, primary_key=True, autoincrement=True)
    account_id    = db.Column(db.Integer, index=True)
    list_media_id = db.Column(db.Integer, index=True)
    create_at     = db.Column(db.DateTime, default=datetime.utcnow)
    update_at     = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Support for
    # - Account.query.get(1).bookmarks
    # - Bookmark.query.get(1).account
    account = db.relationship('Account', backref='bookmarks', primaryjoin="Bookmark.account_id == Account.id", foreign_keys=[account_id])

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

    def __str__(self):
        return self.id

    def __repr__(self):
        return '<Bookmark: %s>' % self.id
