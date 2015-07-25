# coding: utf-8

import requests
from os import path
from time import sleep
from itertools import izip_longest
from multiprocessing import cpu_count
from multiprocessing.dummy import Pool
from .base import BaseCommand
from ..models import db, page_query, ListMedia
from ..helpers.watcher import Watcher

class CheckNotFound(BaseCommand):

    not_found_ids = []

    def __init__(self, logger=None):
        self.logger = self.get_logger() if logger is None else logger

        self.logger.info("CheckNotFound")

    def grouper(self, n, iterable, fillvalue=None):
        "grouper(3, 'ABCDEFG', 'x') --> ABC DEF Gxx"

        args = [iter(iterable)] * n
        return izip_longest(fillvalue=fillvalue, *args)

    def make(self):
        Watcher()

        pool = Pool(cpu_count())

        for media in self.grouper(100, page_query(db.session.query(ListMedia))):
            pool.map(self.check, media)

        pool.close()
        pool.join()

        flush_count = 0
        for media in page_query(db.session.query(ListMedia).filter(ListMedia.id.in_(self.not_found_ids))):
            media.status = "lost"

            db.session.add(media)

            if flush_count % 1000 == 0:
                self.logger.info("--> Flush - flush added data")
                db.session.flush()

            flush_count = flush_count + 1

        db.session.commit()

        self.logger.info("--> Finished")

    def check(self, media):
        try:
            r = requests.head(media.media_url, timeout=3)

            if r.status_code != 200:
                self.logger.info("--> [{0}] - {1}".format(r.status_code, media.media_url))
                self.not_found_ids.append(media.id)
        except:
            self.logger.info("--> Error - {0}".format(media.media_url))
            self.not_found_ids.append(media.id)

        sleep(0.005)
