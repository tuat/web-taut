# coding: utf-8

from .base import BaseCommand
from ..models import ListMedia, db
from ..helpers.value import create_media_hash_id

class HashIdToMedia(BaseCommand):

    def __init__(self, logger=None):
        self.logger = self.get_logger() if logger is None else logger

    def make(self):
        for media in ListMedia.query.yield_per(5):
            media.hash_id = create_media_hash_id(media)

            self.logger.info("Media id: {0} -> {1}".format(media.id, media.hash_id))

            db.session.add(media)

        db.session.commit()
