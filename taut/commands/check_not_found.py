# coding: utf-8

import requests
import threading
import Queue
from os import path
from time import sleep
from itertools import izip_longest
from .base import BaseCommand
from ..models import db, page_query, ListMedia
from ..helpers.watcher import Watcher

class CheckNotFound(BaseCommand):

    def __init__(self, logger=None):
        self.logger        = self.get_logger() if logger is None else logger
        self.not_found_ids = []
        self.url_queue     = Queue.Queue()

        self.logger.info("CheckNotFound")

    def make(self):
        Watcher()
        for i in range(5):
            t = threading.Thread(target=self.worker)
            t.daemon = True
            t.start()

        for media in page_query(db.session.query(ListMedia)):
            self.url_queue.put({
                'id'       : media.id,
                'media_url': media.media_url
            })

        self.url_queue.join()

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

    def worker(self):
        while True:
            media = self.url_queue.get()
            self.check(media)
            self.url_queue.task_done()

    def check(self, media):
        try:
            r = requests.head(media['media_url'], timeout=3)

            if r.status_code != 200:
                self.logger.info("--> [{0}] - {1: >8} - {2}".format(r.status_code, media['id'], media['media_url']))
                self.not_found_ids.append(media['id'])
        except:
            self.logger.info("--> [Err] - {0: >8} - {1}".format(media['id'], media['media_url']))
            self.not_found_ids.append(media['id'])

        sleep(0.005)
