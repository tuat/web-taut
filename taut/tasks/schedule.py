# coding: utf-8

from celery import task
from celery.utils.log import get_task_logger
from ..commands import FetchLists, Sitemap, CheckNotFound, UpdateAvatar

logger = get_task_logger(__name__)

@task
def fetch_lists(list_id, slug):
    logger.info("called schedule.fetch_list")

    FetchLists(list_id, slug, logger).make()

@task
def create_sitemap(offset, limit):
    logger.info("called schedule.create_sitemap, offset: {0}, limit: {1}".format(offset, limit))

    Sitemap(logger).make(offset, limit)

@task
def check_not_found():
    logger.info("called schedule.check_not_found")

    CheckNotFound().make()

@task
def update_avatar():
    logger.info("called schedule.update_avatar")

    UpdateAvatar(logger).make()
