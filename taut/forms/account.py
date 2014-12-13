# coding: utf-8

from wtforms import TextField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, Regexp
from .base import BaseForm
from ..models import Account

class SigninForm(BaseForm):
    account = TextField(
        'Account',
        validators=[
            DataRequired(message="Please enter account name"),
            Length(min=3, max=200)
        ],
    )
    password = PasswordField(
        'Password',
        validators=[
            DataRequired(message="Please enter password")
        ]
    )
    permanent = BooleanField('Remember me')

    def validate_password(self, field):
        account = self.account.data

        if '@' in account:
            user = Account.query.filter_by(email=account).first()
        else:
            user = Account.query.filter_by(username=account).first()

        if not user:
            raise ValueError("Not found account")

        if user.password_verify(field.data):
            self.user = user
            return user
        else:
            raise ValueError("Password incorrect")

class SignupForm(BaseForm):
    username = TextField(
        'Username',
        validators=[
            DataRequired(message='Please enter username'),
            Length(min=3, max=20),
            Regexp(r'^[a-z0-9A-Z]+$', message='Username must english characters only.')
        ]
    )

    email = TextField(
        'Email',
        validators=[
            DataRequired(message='Please enter email'),
            Email(message='Invalid email format')
        ]
    )

    password = PasswordField(
        'Password',
        validators=[
            DataRequired(message='Please enter password'),
            Length(message="Password must more than 8 length", min=8),
            EqualTo('confirm_password', message='Passwords must match'),
        ]
    )

    confirm_password = PasswordField('Confirm Password')

    def validate_username(self, field):
        if Account.query.filter_by(username=field.data.lower()).count():
            raise ValueError('This username has been registered.')

    def validate_email(self, field):
        if Account.query.filter_by(email=field.data.lower()).count():
            raise ValueError('This email has been registered.')

    def save(self):
        data = self.data
        data.pop('confirm_password', None)

        user = Account(**data)
        user.save()

        return user
