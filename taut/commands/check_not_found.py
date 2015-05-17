# coding: utf-8

import requests
from os import path
from time import sleep
from multiprocessing import cpu_count
from multiprocessing.dummy import Pool
from .base import BaseCommand
from ..models import db, ListMedia
from ..helpers.watcher import Watcher

class CheckNotFound(BaseCommand):

    not_found_ids = []

    def __init__(self, logger=None):
        self.logger = self.get_logger() if logger is None else logger

        self.logger.info("CheckNotFound")

    def make(self):
        medias = ListMedia.query.filter_by(status="show").all()

        Watcher()
        pool = Pool(cpu_count())
        pool.map(self.check, medias)
        pool.close()
        pool.join()

        for media_id in self.not_found_ids:
            media = ListMedia.query.get(media_id)
            media.status = "lost"

            db.session.add(media)

        db.session.commit()

    def check(self, media):
        try:
            r = requests.head(media.media_url, timeout=3)

            if r.status_code != 200:
                self.logger.debug("--> [{0}] - {1}".format(r.status_code, media.media_url))
                self.not_found_ids.append(media.id)
        except:
            self.logger.debug("--> Error - {0}".format(media.media_url))
            self.not_found_ids.append(media.id)

        sleep(0.005)
