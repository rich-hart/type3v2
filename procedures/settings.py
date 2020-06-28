from django.conf.settings import *
# CELERY STUFF
CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL', 'amqp://guest:guest@localhost:5672//')
CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND','amqp://guest:guest@localhost:5672//')
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
