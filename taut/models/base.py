# coding: utf-8

import os
import datetime
from flask.ext.sqlalchemy import SQLAlchemy

if "USE_PSYCOGREEN" in os.environ:
    from gevent.monkey import patch_all
    from psycogreen.gevent import patch_psycopg

    patch_all()
    patch_psycopg()

class SessionMixin(object):
    def save(self):
        db.session.add(self)
        db.session.commit()
        return self

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return self

db = SQLAlchemy()
