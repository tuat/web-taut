# coding: utf-8

from os import path
from flask import current_app, url_for, render_template
from .base import BaseCommand

class Robots(BaseCommand):

    def __init__(self, logger=None):
        self.logger = self.get_logger() if logger is None else logger

        self.logger.info("Robots")

    def make(self):
        sitemaps = (
            "{0}/sitemap-media.xml".format(url_for('index.index', _external=True)),
            "{0}/sitemap-profile.xml".format(url_for('index.index', _external=True))
        )

        robots    = render_template('robots.txt', sitemaps=sitemaps)
        save_path = path.join(current_app.static_folder, 'robots.txt')

        self.logger.info("---> creating robots.txt to {0}".format(save_path))

        with open(save_path, 'w') as f:
            f.write(robots)
            f.close()
