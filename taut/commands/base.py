# coding: utf-8

import logging

class BaseCommand(object):

    def get_logger(self):
        logging.getLogger("requests").setLevel(logging.WARNING)

        logger = logging.getLogger(__name__)
        logger.setLevel(logging.DEBUG)

        logger_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        logger_stream_handler = logging.StreamHandler()
        logger_stream_handler.setLevel(logging.DEBUG)
        logger_stream_handler.setFormatter(logger_formatter)
        logger.addHandler(logger_stream_handler)

        return logger
