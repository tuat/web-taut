# coding: utf-8

from datetime import datetime
from .base import db, SessionMixin

class AccountConnection(db.Model, SessionMixin):
    id               = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id          = db.Column(db.Integer)
    provider_name    = db.Column(db.String(30))
    provider_user_id = db.Column(db.String(30))
    access_token     = db.Column(db.String(80))
    display_name     = db.Column(db.String(50))
    profile_url      = db.Column(db.String(180))
    avatar_url       = db.Column(db.String(180))
    create_at        = db.Column(db.DateTime, default=datetime.utcnow)
    update_at        = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __init__(self, **kwargs):
        if 'provider_name' not in kwargs:
            self.provider_name = kwargs.pop('provider_name').lower()

        for k, v in kwargs.items():
            setattr(self, k, v)

    def __str__(self):
        return self.id

    def __repr__(self):
        return '<AccountConnection: %s>' % self.id
