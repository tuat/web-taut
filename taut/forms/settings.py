# coding: utf-8

from flask import g
from wtforms import TextField, PasswordField
from wtforms.validators import DataRequired, Regexp, Length, EqualTo
from .base import BaseForm
from ..models import Account

class ProfileForm(BaseForm):
    username = TextField(
        'Username',
        validators=[
            DataRequired(message="Please enter username"),
            Regexp(r'^[a-z0-9A-Z]+$', message="English characters only"),
            Length(min=3, max=80),
        ]
    )

    def validate_username(self, field):
        if Account.query.filter_by(username=field.data.lower()).count():
            raise ValueError('Username already registered')

class PasswordForm(BaseForm):
    old_password = PasswordField(
        'Old Password',
        validators=[
            DataRequired(message="Please enter old password")
        ]
    )

    new_password = PasswordField(
        'New Password',
        validators=[
            DataRequired(message='Please enter new password'),
            Length(message="New password must more than 8 length", min=8),
            EqualTo('confirm_new_password', message='New password must match'),
        ]
    )

    confirm_new_password = PasswordField('Confirm New Password')

    def validate_old_password(self, field):
        account = Account.query.filter_by(username=g.user.username).first()

        if account.password_verify(field.data.lower()) is False:
            raise ValueError("Password incorrect")
