from celery import Celery
from celery.schedules import crontab

celery_app = Celery('app', include=['app.tasks'])
celery_app.config_from_object('app.celeryconfig')

celery_app.conf.beat_schedule = {
    'update_every_day': {
        'task': 'app.tasks.update_items',
        'schedule': crontab(hour=7, minute=30, day_of_week=6),
    },
}
