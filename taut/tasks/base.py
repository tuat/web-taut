# coding: utf-8

from ..app import create_app
from ..models import db
from celery import Celery
from multiprocessing.util import register_after_fork

def create_celery_app(app=None, enable_route=True):
    app = app or create_app(enable_route=enable_route)

    # try to fix SSL SYSCALL error
    register_after_fork(db.engine, db.engine.dispose)

    celery = Celery()
    celery.conf.update(app.config)

    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask

    return celery
