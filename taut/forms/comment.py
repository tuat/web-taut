# coding: utf-8

from .base import BaseForm
from wtforms import TextAreaField
from wtforms.validators import Required
from ..models import Comment

class CommentForm(BaseForm):
    content = TextAreaField(
        'Content',
        validators=[
            Required(message='Please enter content')
        ]
    )

    def save(self, list_media_id, account):
        comment = Comment(**self.data)
        comment.list_media_id = list_media_id
        comment.account_id    = account.id
        comment.save()

        return comment
