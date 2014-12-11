# coding: utf-8

import os
from TwitterAPI import TwitterAPI
from flask import current_app
from .base import BaseCommand
from ..models import ListUser, ListTweet, ListMedia

class FetchLists(BaseCommand):

    def __init__(self, list_id, slug, logger=None):
        self.logger = self.get_logger() if logger is None else logger

        twitter = current_app.config.get('TWITTER')

        self.api = TwitterAPI(
            consumer_key=twitter['consumer_key'],
            consumer_secret=twitter['consumer_secret'],
            access_token_key=twitter['access_token_key'],
            access_token_secret=twitter['access_token_secret']
        )

        self.list_id = list_id
        self.slug    = slug

    def make(self):
        params = {
            "list_id": self.list_id,
            "slug": self.slug,
        }

        twitter_list_last_id_filename = current_app.config.get('TWITTER_LIST_LAST_ID_FILENAME')
        if (os.path.exists(twitter_list_last_id_filename)):
            since_id = open(twitter_list_last_id_filename).read().strip()

            if len(since_id) > 0:
                params['since_id'] = since_id

                self.logger.info("last id: {0}".format(since_id))

        lists_statuses = self.api.request("lists/statuses", params)
        lists_last_id  = None

        for item in lists_statuses:
            self.logger.info("lists.item: {0}".format(item['id']))

            if not lists_last_id:
                lists_last_id = item['id']

            if 'extended_entities' in item:
                self.logger.info("---> extended_entities : yes")

                extended_entities = item['extended_entities']

                if 'media' in extended_entities:
                    self.logger.info("---> media : yes")

                    # Data
                    id_str      = item['id_str']
                    name        = item['user']['name']
                    screen_name = item['user']['screen_name']

                    # User
                    list_user = ListUser.query.filter_by(screen_name=screen_name).first()

                    if not list_user:
                        self.logger.info("---> new user : yes")

                        list_user                   = ListUser()
                        list_user.name              = name
                        list_user.screen_name       = screen_name
                        list_user.profile_image_url = item['user']['profile_image_url']
                        list_user.save()
                    else:
                        self.logger.info("---> new user : no")

                    # Tweet
                    list_tweet = ListTweet.query.filter_by(id_str=id_str).first()

                    if not list_tweet:
                        self.logger.info("---> new tweet : yes")

                        list_tweet              = ListTweet()
                        list_tweet.id_str       = id_str
                        list_tweet.list_user_id = list_user.id
                        list_tweet.text         = item['text']
                        list_tweet.save()

                        # Tweet media
                        for media in extended_entities['media']:
                            media_id_str = media['id_str']
                            media_url    = media['media_url']

                            list_media   = ListMedia.query.filter(
                                (ListMedia.id_str == media_id_str) |
                                (ListMedia.media_url == media_url)
                            ).first()

                            if not list_media:
                                self.logger.info("---> new media : yes")

                                list_media               = ListMedia()
                                list_media.list_user_id  = list_user.id
                                list_media.list_tweet_id = list_tweet.id
                                list_media.id_str        = media_id_str
                                list_media.media_url     = media_url
                                list_media.type          = media['type']
                                list_media.save()
                            else:
                                self.logger.info("---> new media : no")
                    else:
                        self.logger.info("---> new tweet : no")

        f = open(twitter_list_last_id_filename, 'w+')
        f.write(str(lists_last_id))
        f.close()
