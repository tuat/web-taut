#!/usr/bin/env python

from flask_script import Manager, Server
from taut.app import create_app

app = create_app()

manager = Manager(app)
manager.add_command('runserver', Server())

@manager.command
def createdb():
    """Create the database"""
    from taut.models import db

    db.create_all()

@manager.command
def runtask(name=None):
    """Run task server"""
    from celery.bin.worker import worker
    from celery.bin.beat import beat

    log_level = app.config.get('CELERY_LOG_LEVEL')

    if name == 'celery':
        worker = worker(app=app.celery)
        worker.run(loglevel=log_level)
    elif name == 'beat':
        beat = beat(app=app.celery)
        beat.run(loglevel=log_level)
    elif name == 'all':
        worker = worker(app=app.celery)
        worker.run(loglevel=log_level, beat=True)
    else:
        print("Usage: python manager.py runtask -n [celery | beat | all]")

@manager.command
def testfetchlists():
    from taut.commands.fetch_lists import FetchLists

    FetchLists(LIST_ID, SLUG).make()

if __name__ == '__main__':
    manager.run()
