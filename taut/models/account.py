# coding: utf-8

from datetime import datetime
from flask.ext.bcrypt import Bcrypt
from .base import SessionMixin, db

class Account(db.Model, SessionMixin):
    id            = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username      = db.Column(db.String(30), nullable=False, unique=True, index=True)
    email         = db.Column(db.String(80), nullable=False, unique=True, index=True)
    password      = db.Column(db.String(100), nullable=False)
    role          = db.Column(db.String(10), default='user')
    create_at     = db.Column(db.DateTime, default=datetime.utcnow)
    update_at     = db.Column(db.DateTime, onupdate=datetime.utcnow)

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

    def __str__(self):
        return self.media_url

    def __repr__(self):
        return '<ListMedia: %s>' % self.id

    def password_verify(self, password):
        return Bcrypt().check_password_hash(self.password, password)
