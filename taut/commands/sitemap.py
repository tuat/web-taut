# coding: utf-8

from os import path
from datetime import datetime
from dateutil import tz
from time import sleep
from werkzeug.routing import BuildError
from flask import g, current_app, url_for, render_template
from ..models import ListMedia, ListUser
from ..helpers.value import thumb, url_for_media_detail
from .base import BaseCommand

class Sitemap(BaseCommand):

    def __init__(self, logger=None):
        self.logger = self.get_logger() if logger is None else logger

        self.logger.info("Sitemap")

    def generate_media(self, offset, limit):
        self.logger.info("# Generate media ({0}, {1})".format(offset, limit))

        list_medias = ListMedia.query.filter(ListMedia.status == 'show').order_by(ListMedia.create_at.desc()).offset(offset).limit(limit).all()
        media_pages = []

        for list_media in list_medias:
            if list_media.hash_id:
                media_pages.append({
                    'url'      : url_for_media_detail(list_media, _external=True),
                    'image'    : thumb(list_media.media_url, 500, 500),
                    'create_at': list_media.create_at.replace(tzinfo=tz.tzlocal()).isoformat(),
                })

        self.logger.info("---> total pages: {0}".format(len(media_pages)))

        if media_pages:
            sitemap   = render_template('sitemap/media.xml', pages=media_pages)
            save_path = path.join(current_app.static_folder, 'sitemap-media.xml')

            self.logger.info("---> creating sitemap-media.xml to {0}".format(save_path))

            with open(save_path, 'w') as f:
                f.write(sitemap)
                f.close()

    def generate_profile(self, offset, limit):
        self.logger.info("# Generate media ({0}, {1})".format(offset, limit))

        list_users  = ListUser.query.order_by(ListUser.create_at.desc()).offset(offset).limit(limit).all()
        media_pages = []

        for list_user in list_users:
            media_pages.append({
                'url'      : url_for('people.profile', screen_name=list_user.screen_name, _external=True),
                'image'    : list_user.profile_image_url,
                'create_at': list_user.create_at.replace(tzinfo=tz.tzlocal()).isoformat(),
            })

        self.logger.info("---> total pages: {0}".format(len(media_pages)))

        if media_pages:
            sitemap   = render_template('sitemap/profile.xml', pages=media_pages)
            save_path = path.join(current_app.static_folder, 'sitemap-profile.xml')

            self.logger.info("---> creating sitemap-profile.xml to {0}".format(save_path))

            with open(save_path, 'w') as f:
                f.write(sitemap)
                f.close()

    def make(self, offset=0, limit=10000):
        self.generate_media(offset, limit)
        self.generate_profile(offset, limit)
