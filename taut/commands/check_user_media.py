# coding: utf-8

from concurrent import futures
import requests
from time import sleep
from .base import BaseCommand
from ..models import db, ListMedia

class CheckUserMedia(BaseCommand):

    not_found_urls = []

    def __init__(self, logger=None):
        self.logger = self.get_logger() if logger is None else logger

        self.logger.info("CheckUserMedia")

    def load_url(self, url, timeout):
        try:
            r = requests.head(url, timeout=timeout)

            if r.status_code != 200:
                self.logger.info("--> {0} - [{0}]".format(url, r.status_code))
                self.not_found_urls.append(media.id)
        except:
            self.logger.info("--> {0} - [Exception]".format(url))
            self.not_found_urls.append(url)

        sleep(0.015)

    def make(self):
        # Group the media urls by user id
        media_table = ListMedia.query.order_by(ListMedia.create_at.desc()).subquery()
        list_medias = db.session.query(
            media_table.c.list_user_id,
            db.func.group_concat(media_table.c.media_url).label('media_urls'),
        ).group_by(media_table.c.list_user_id)

        # Check 100 media in each user is or not found
        for media in list_medias.yield_per(5):
            urls = media.media_urls.split(',')[0:100]

            self.logger.info('user_id: {0}, total: {1}'.format(media.list_user_id, len(urls)))

            with futures.ThreadPoolExecutor(max_workers=5) as executor:
                future_to_url = {
                    executor.submit(self.load_url, url, 60): url for url in urls
                }

                for future in futures.as_completed(future_to_url):
                    url = future_to_url[future]

                    try:
                        data = future.result()
                    except Exception as exc:
                        self.logger.info('--> {0} generated an exception: {1}'.format(url, exc))
                    else:
                        self.logger.info('--> {0} fetched'.format(url))

                self.logger.info("--> finished")

            sleep(1)

        # Mark as lost in all not found urls
        for url in self.not_found_urls:
            media = ListMedia.query.filter(ListMedia.media_url == url).first()
            media.status = "lost"

            db.session.add(media)

        db.session.commit()
