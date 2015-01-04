# coding: utf-8

from os import path
from datetime import datetime
from dateutil import tz
from flask import g, current_app, url_for, render_template
from ..models import ListMedia
from ..helpers.value import thumb
from .base import BaseCommand

class Sitemap(BaseCommand):

    def __init__(self, logger=None):
        self.logger = self.get_logger() if logger is None else logger

        self.logger.info("Sitemap")

    def make(self, offset=0, limit=10000):
        list_medias = ListMedia.query.order_by(ListMedia.create_at.desc()).offset(offset).limit(limit).all()

        pages = []

        for list_media in list_medias:
            pages.append({
                'url'      : url_for('media.detail', list_media_id=list_media.id, _external=True),
                'image'    : thumb(list_media.media_url, 500, 500),
                'create_at': list_media.create_at.replace(tzinfo=tz.tzlocal()).isoformat(),
            })

        sitemap   = render_template('sitemap.xml', pages=pages)
        save_path = path.join(current_app.static_folder, 'sitemap.xml')

        self.logger.info("===> creating sitemap.xml to {0}".format(save_path))

        with open(save_path, 'w') as f:
            f.write(sitemap)
            f.close()