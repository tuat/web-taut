# coding: utf-8

from os import path
from time import sleep
from TwitterAPI import TwitterAPI
from flask import current_app
from .base import BaseCommand
from ..models import db, ListUser, ListTweet, ListMedia
from ..helpers.value import create_media_hash_id

class FetchLists(BaseCommand):

    def __init__(self, list_id, slug, logger=None):
        # Initial logger and check input arguments
        self.logger = self.get_logger() if logger is None else logger

        if list_id is None or slug is None:
            self.logger.error("Please provide the `--list_id` and `--slug` arguments")
        else:
            self.logger.info("The list_id and slug are {0} and {1}".format(list_id, slug))

            # Set the arguments to class property
            self.list_id = list_id
            self.slug    = slug

            # Initial twitter api and read config
            self.twitter                       = current_app.config.get('TWITTER')
            self.twitter_list_last_id_filename = current_app.config.get('TWITTER_LIST_LAST_ID_FILENAME')

            self.twitter_api = TwitterAPI(
                consumer_key        = self.twitter['consumer_key'],
                consumer_secret     = self.twitter['consumer_secret'],
                access_token_key    = self.twitter['access_token_key'],
                access_token_secret = self.twitter['access_token_secret']
            )

    def get_since_id(self):
        if path.exists(self.twitter_list_last_id_filename):
            since_id = open(self.twitter_list_last_id_filename).read().strip()

            if len(since_id) > 0:
                return since_id
            else:
                return None
        else:
            return None

    def add_new_users(self, list_users):
        self.logger.info("Add new users")

        # Find out new user by compare screen name
        screen_names = [list_user['user_screen_name'] for id_str, list_user in list_users.items()]

        if not screen_names:
            self.logger.info("---> the new users table is empty, skipped")
        else:
            exists_users        = ListUser.query.filter(ListUser.screen_name.in_(screen_names)).all()
            exists_screen_names = set([user.screen_name for user in exists_users])
            new_screen_names    = [screen_name for screen_name in screen_names if screen_name not in exists_screen_names]

            # Add new user to database
            for id_str, list_user in list_users.items():
                name              = list_user['user_name']
                screen_name       = list_user['user_screen_name']
                profile_image_url = list_user['user_profile_image_url']

                if screen_name in new_screen_names:
                    list_user                   = ListUser()
                    list_user.name              = name
                    list_user.screen_name       = screen_name
                    list_user.profile_image_url = profile_image_url

                    db.session.add(list_user)

                    self.logger.info("---> screen_name: {0}, added".format(screen_name))
                else:
                    self.logger.info("---> screen_name: {0}, skipped".format(screen_name))

            db.session.commit()

    def add_new_tweets(self, list_tweets):
        self.logger.info("Add new tweets")

        # Find out new tweet by compare id str
        id_strs = [id_str for id_str in list_tweets]

        if not id_strs:
            self.logger.info("---> the new tweet table is empty, skipped")
        else:
            exists_tweets  = ListTweet.query.filter(ListTweet.id_str.in_(id_strs)).all()
            exists_id_strs = set([tweet.id_str for tweet in exists_tweets])
            new_id_strs    = [id_str for id_str in id_strs if id_str not in exists_id_strs]

            # Find out related user by screen name
            screen_names = [list_tweet['user_screen_name'] for id_str, list_tweet in list_tweets.items()]
            list_users   = ListUser.query.filter(ListUser.screen_name.in_(screen_names)).all()
            user_mapper  = {}

            for list_user in list_users:
                user_mapper[list_user.screen_name] = list_user

            # Add new tweet to database
            for id_str, list_tweet in list_tweets.items():
                text        = list_tweet['text']
                screen_name = list_tweet['user_screen_name']

                if id_str in new_id_strs:
                    list_tweet              = ListTweet()
                    list_tweet.id_str       = id_str
                    list_tweet.list_user_id = user_mapper[screen_name].id
                    list_tweet.text         = text

                    db.session.add(list_tweet)

                    self.logger.info("--> id_str: {0}, added".format(id_str))
                else:
                    self.logger.info("--> id_str: {0}, skipped".format(id_str))

            db.session.commit()

    def add_new_medias(self, list_medias):
        self.logger.info("Add new medias")

        # Find out new media by media id str and url
        media_id_strs = [media['media_id_str'] for id_str, media in list_medias.items()]
        media_urls    = [media['media_url'] for id_str, media in list_medias.items()]

        if not media_id_strs and not media_urls:
            self.logger.info("---> the new users table is empty, skipped")
        else:
            exists_medias        = ListMedia.query.filter(ListMedia.id_str.in_(media_id_strs) | ListMedia.media_url.in_(media_urls)).all()
            exists_media_id_strs = set([media.id_str for media in exists_medias])
            exists_media_urls    = set([media.media_url for media in exists_medias])
            new_media_id_strs    = [media_id_str for media_id_str in media_id_strs if media_id_str not in exists_media_id_strs]
            new_media_urls       = [media_url for media_url in media_urls if media_url not in exists_media_urls]

            # Find out related tweet by id str
            tweet_id_strs = [id_str for id_str, list_media in list_medias.items()]
            list_tweets   = ListTweet.query.filter(ListTweet.id_str.in_(tweet_id_strs)).all()
            tweet_mapper  = {}

            for list_tweet in list_tweets:
                tweet_mapper[list_tweet.id_str] = list_tweet

            # Find out related user by screen name
            user_screen_names = [list_media['user_screen_name'] for id_str, list_media in list_medias.items()]
            list_users        = ListUser.query.filter(ListUser.screen_name.in_(user_screen_names)).all()
            user_mapper       = {}

            for list_user in list_users:
                user_mapper[list_user.screen_name] = list_user

            # Add new media to database
            for id_str, list_media in list_medias.items():
                user_screen_name = list_media['user_screen_name']
                media_id_str     = list_media['media_id_str']
                media_url        = list_media['media_url']
                media_type       = list_media['media_type']

                if media_id_str in new_media_id_strs and media_url in new_media_urls:
                    list_media               = ListMedia()
                    list_media.list_user_id  = user_mapper[user_screen_name].id
                    list_media.list_tweet_id = tweet_mapper[id_str].id
                    list_media.id_str        = media_id_str
                    list_media.media_url     = media_url
                    list_media.type          = media_type

                    db.session.add(list_media)

                    self.logger.info("--> media id str: {0}, added".format(media_id_str))
                else:
                    self.logger.info("--> media id str: {0}, skipped".format(media_id_str))

            db.session.commit()

    def update_new_media_hash_ids(self):
        self.logger.info("Update new media hash ids")

        list_medias = ListMedia.query.filter(ListMedia.hash_id.is_(None)).all()

        for list_media in list_medias:
            list_media.hash_id = create_media_hash_id(list_media)

            self.logger.info("---> list media: {0} -> {1}".format(list_media.id, list_media.hash_id))

            db.session.add(list_media)

        db.session.commit()

    def make(self):
        # Set default query string table
        default_query_strings = dict(
            slug     = self.slug,
            list_id  = self.list_id
        )

        # Check since id is or not eixsts before ran other action
        since_id = self.get_since_id()

        if not since_id:
            self.logger.error("Can not found the since id from file")
        else:
            # Add since id to default query string table
            self.logger.info("The since_id is {0}".format(since_id))

            default_query_strings['since_id'] = since_id

            # Make request to get latest feeds
            lists_statuses = self.twitter_api.request("lists/statuses", default_query_strings)
            lists_last_id  = None

            list_users  = {}
            list_tweets = {}
            list_medias = {}

            # Lookup all list statuses
            self.logger.info("Read list statues")

            for item in lists_statuses:
                self.logger.info("# item: {0}".format(item['id']))

                # Initial last id
                if not lists_last_id:
                    lists_last_id = item['id']

                # Find extended entities in list item
                if 'extended_entities' in item:
                    self.logger.info("---> extended_entities : yes")

                    extended_entities = item['extended_entities']

                    # Find medas in extended entity
                    if 'media' in extended_entities:
                        self.logger.info("---> media : yes")

                        # Get list item base information
                        id_str                 = item['id_str']
                        user_name              = item['user']['name']
                        user_screen_name       = item['user']['screen_name']
                        user_profile_image_url = item['user']['profile_image_url']
                        text                   = item['text']

                        # Add current user information into users table to find out which is new user
                        list_users[id_str] = dict(
                            user_name              = user_name,
                            user_screen_name       = user_screen_name,
                            user_profile_image_url = user_profile_image_url
                        )

                        # Add current tweet information into tweets table to find out which is new tweet
                        list_tweets[id_str] = dict(
                            text             = text,
                            user_screen_name = user_screen_name
                        )

                        # Find media in tweet
                        for media in extended_entities['media']:
                            media_id_str = media['id_str']
                            media_url    = media['media_url']
                            media_type   = media['type']

                            # Add current media information into medias table to find out which is new media
                            list_medias[id_str] = dict(
                                user_screen_name = user_screen_name,
                                media_id_str     = media_id_str,
                                media_url        = media_url,
                                media_type       = media_type,
                            )

                sleep(1)

            # Add new user from users table
            self.add_new_users(list_users)

            # Add new tweet from tweets table
            self.add_new_tweets(list_tweets)

            # Add new media from medias table
            self.add_new_medias(list_medias)

            # Update new media hash id from database
            self.update_new_media_hash_ids()

            # Store last id into file
            if lists_last_id:
                f = open(self.twitter_list_last_id_filename, 'w+')
                f.write(str(lists_last_id))
                f.close()
