# coding: utf-8

import requests
from os import path
from multiprocessing import cpu_count
from multiprocessing.dummy import Pool
from time import sleep
from itertools import izip_longest
from .base import BaseCommand
from ..models import db, page_query, ListMedia
from ..helpers.watcher import Watcher

class CheckOldMedia(BaseCommand):

    def __init__(self, logger=None):
        self.logger         = self.get_logger() if logger is None else logger
        self.media_urls     = []
        self.lost_media_ids = []

        self.logger.info("CheckOldMedia")

    def make(self, offset_size=0, limit_size=1000):
        self.logger.info("---> offset: {0}, limit: {1}".format(offset_size, limit_size))

        list_medias = ListMedia.query.filter(ListMedia.status == "show").order_by(ListMedia.create_at.desc()).offset(offset_size).limit(limit_size).all()

        for media in list_medias:
            self.media_urls.append({
                'id'  : media.id,
                'link': media.media_url
            })

        Watcher()
        pool = Pool(cpu_count())
        pool.map(self.check, self.media_urls)
        pool.close()
        pool.join()

        flush_count = 0
        for media in page_query(db.session.query(ListMedia).filter(ListMedia.id.in_(self.lost_media_ids))):
            media.status = "lost"

            db.session.add(media)

            if flush_count % 1000 == 0:
                self.logger.info("--> Flush - flush added data")
                db.session.flush()

            flush_count = flush_count + 1

        db.session.commit()

        self.logger.info("--> Finished")

    def check(self, media_url):
        try:
            r = requests.head(media_url['link'], timeout=3)

            if r.status_code != 200:
                self.logger.info("--> [{0}] - {1: >8} - {2}".format(r.status_code, media_url['id'], media_url['link']))
                self.lost_media_ids.append(media_url['id'])
        except:
            self.logger.info("--> [Err] - {0: >8} - {1}".format(media_url['id'], media_url['link']))
            self.lost_media_ids.append(media_url['id'])

        sleep(0.005)
