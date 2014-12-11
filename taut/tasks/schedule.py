# coding: utf-8

from celery import task
from celery.utils.log import get_task_logger
from ..commands import FetchLists

logger = get_task_logger(__name__)

@task
def fetch_lists(list_id, slug):
    logger.info("called schedule.fetch_list")

    FetchLists(list_id, slug, logger).make()
