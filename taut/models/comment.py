# coding: utf-8

from .base import db, SessionMixin
from datetime import datetime

class Comment(db.Model, SessionMixin):
    id            = db.Column(db.Integer, primary_key=True, autoincrement=True)
    account_id    = db.Column(db.Integer, nullable=False)
    list_media_id = db.Column(db.Integer, nullable=False)
    content       = db.Column(db.Text)
    create_at     = db.Column(db.DateTime, default=datetime.utcnow)
    update_at     = db.Column(db.DateTime, onupdate=datetime.utcnow)

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

    def __str__(self):
        return self.content

    def __repr__(self):
        return '<Comment: %s>' % self.id

    def to_json(self, user=None):
        default_dict = {
            'id'        : self.id,
            'content'   : self.content
        }

        if user is None:
            default_dict['user'] = {
                'id': self.account_id
            }
        else:
            default_dict['user'] = user.to_json()

        return default_dict
