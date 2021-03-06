#!/usr/bin/env python

from flask_script import Manager, Server
from flask_assets import ManageAssets
from taut.app import create_app

app = create_app()

manager = Manager(app)
manager.add_command('runserver', Server())
manager.add_command("assets", ManageAssets())

@manager.command
def createdb():
    """Create the database"""
    from taut.models import db

    db.create_all()

@manager.command
def genpw(password):
    """Genernate password"""

    from flask_bcrypt import Bcrypt

    print(Bcrypt(app).generate_password_hash(password))

@manager.command
def gensitemap():
    """Generate sitemap"""
    from taut.commands.sitemap import Sitemap

    Sitemap().make(0, 10000)

@manager.command
def genrobots():
    """Generate robots.txt"""
    from taut.commands.robots import Robots

    Robots().make()

@manager.command
def testcommands(name=None, list_id=None, slug=None):
    from taut.models.base import db

    db.engine.dispose()

    """Test commands"""
    if name == 'fetchlists':
        from taut.commands.fetch_lists import FetchLists
        FetchLists(list_id, slug).make()
    elif name == 'checkoldmedia':
        from taut.commands.check_old_media import CheckOldMedia
        CheckOldMedia().make()
    elif name == 'updateprofile':
        from taut.commands.update_profile import UpdateProfile
        UpdateProfile().make()
    elif name == 'checkusermedia':
        from taut.commands.check_user_media import CheckUserMedia
        CheckUserMedia().make()
    else:
        print("Usage: python manager.py testcommands -n [fetchlists | checkoldmedia | updateprofile | checkusermedia]")

@manager.command
def genhashid2media():
    """Generate hash id to list media"""
    from taut.commands.hash_id_to_media import HashIdToMedia

    HashIdToMedia().make()

@manager.command
def callsitemaptask():
    from taut.tasks.base import create_celery_app

    celery = create_celery_app(app)
    celery.send_task("taut.tasks.schedule.create_sitemap", args=(0, 1000))

if __name__ == '__main__':
    manager.run()
