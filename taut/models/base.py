# coding: utf-8

import os
import datetime
from flask_sqlalchemy import SQLAlchemy

if "USE_PSYCOGREEN" in os.environ:
    from gevent.monkey import patch_all
    from psycogreen.gevent import patch_psycopg

    patch_all()
    patch_psycopg()

def page_query(query, limit_size=1000):
    offset = 0

    while True:
        r = False

        for element in query.offset(offset).limit(limit_size):
            r = True

            yield element

        offset += 1000

        if not r:
            break

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
