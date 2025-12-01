import os
from typing import Any

from celery import Celery
from celery.schedules import crontab

from api.tasks import heartbeat, scrape

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

app = Celery('trialsource-backend')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')
#
# Load task modules from all registered Django apps.
app.autodiscover_tasks()


@app.on_after_finalize.connect
def setup_periodic_tasks(sender: Celery, **kwargs: dict[str, Any]) -> None:
    # Calls heartbeat() every 120 seconds.
    sender.add_periodic_task(1800.0, heartbeat.s(), name='Heartbeat every 30 minutes')

    # # Calls test('hello') every 30 seconds.
    # # It uses the same signature of previous task, an explicit name is
    # # defined to avoid this task replacing the previous one defined.
    # sender.add_periodic_task(20.0, test.s('hello'), name='add every 20')

    # # Calls test('world') every 30 seconds
    # sender.add_periodic_task(30.0, test.s('world'), expires=10)

    # Executes every Monday morning at 7:30 a.m.
    sender.add_periodic_task(
        crontab(hour=5, minute=7),
        scrape.s(),
        name='Scraper'
    )

@app.task
def test(arg: Any) -> None:
    print(arg)