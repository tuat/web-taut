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

if __name__ == '__main__':
    manager.run()
