from ..models import db
from celery.signals import task_prerun
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)

@task_prerun.connect
def on_task_pre_run(sender=None, task_id=None, task=None, args=None, **kwargs):
    logger.info("Pre-run: all, Action: close db connection, Task name: {0}".format(task.name))

    db.engine.dispose()
