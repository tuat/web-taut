# coding: utf-8

from wtforms import TextField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length
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

