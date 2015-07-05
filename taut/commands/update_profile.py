# coding: utf-8

from flask import current_app
from TwitterAPI import TwitterAPI
from .base import BaseCommand
from ..models import ListUser, db

class UpdateProfile(BaseCommand):

    def __init__(self, logger=None):
        self.logger = self.get_logger() if logger is None else logger

        twitter = current_app.config.get('TWITTER')

        self.api = TwitterAPI(
            consumer_key=twitter['consumer_key'],
            consumer_secret=twitter['consumer_secret'],
            access_token_key=twitter['access_token_key'],
            access_token_secret=twitter['access_token_secret']
        )

    def update(self, page):
        self.logger.info("page: {0}".format(page))

        users         = ListUser.query.paginate(page, 100)
        screen_names  = ','.join([user.screen_name for user in users.items])
        parameters    = { "screen_name": screen_names }
        twitter_users = self.api.request("users/lookup", parameters)

        for twitter_user in twitter_users:

            name              = twitter_user['name']
            screen_name       = twitter_user['screen_name']
            profile_image_url = twitter_user['profile_image_url']

            self.logger.info("{0} - {1}".format(screen_name, profile_image_url))

            user                   = ListUser.query.filter_by(screen_name=screen_name).first()
            user.name              = name
            user.profile_image_url = profile_image_url

            db.session.add(user)

        db.session.commit()

        if users.has_next:
            self.update(page + 1)

    def make(self):
        self.update(1)
