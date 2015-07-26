# coding: utf-8

from celery.utils.log import get_task_logger
from .base import create_celery_app
from ..commands import FetchLists, Sitemap, CheckOldMedia, UpdateProfile, CheckUserMedia

celery = create_celery_app()
logger = get_task_logger(__name__)

@celery.task
def fetch_lists(list_id, slug):
    logger.info("called schedule.fetch_list")

    FetchLists(list_id, slug, logger).make()

@celery.task
def create_sitemap(offset, limit):
    logger.info("called schedule.create_sitemap, offset: {0}, limit: {1}".format(offset, limit))

    Sitemap(logger).make(offset, limit)

@celery.task
def check_old_media():
    logger.info("called schedule.check_user_media")

    CheckOldMedia().make()

@celery.task
def update_profile():
    logger.info("called schedule.update_profile")

    UpdateProfile(logger).make()

@celery.task
def check_user_media():
    logger.info("called schedule.check_user_media")

    CheckUserMedia().make()
