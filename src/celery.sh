celery -A app.celery beat -l info &
celery -A app.celery worker -l info