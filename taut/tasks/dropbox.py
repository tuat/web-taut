# coding: utf-8

from __future__ import absolute_import
import os
from dropbox import client
# from celery import task
from celery.utils.log import get_task_logger
from .base import create_celery_app
from ..helpers.dropbox import download_image
from ..models import AccountConnection

celery = create_celery_app(enable_route=False)
logger = get_task_logger(__name__)

@celery.task
def sync_media_image(user_id, list_media_id, list_user_screen_name):
    logger.info("called dropbox.sync_media_image (list media id: {0})".format(list_media_id))

    saved_file         = download_image(list_media_id, list_user_screen_name)
    account_connection = AccountConnection.query.filter_by(user_id=user_id, provider_name='dropbox').first()
    status             = 'faield'

    logger.info("==> saved_file: {0}".format(saved_file))
    logger.info("==> account_connection: {0}".format('PASS' if account_connection.access_token != '' else 'Failed'))

    if saved_file and account_connection and account_connection.access_token != '':
        dropbox_client = client.DropboxClient(account_connection.access_token)

        dropbox_client.put_file(
            '/{0}/{1}'.format(list_user_screen_name, os.path.basename(saved_file)),
            open(saved_file),
            overwrite=True
        )

        status = 'success'

        logger.info("==> Saved")
    else:
        logger.info("==> Failed")
