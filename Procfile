release: python manage.py migrate
web: gunicorn oh_template.wsgi --log-file=-
worker: celery worker -A oh_template --concurrency 1
