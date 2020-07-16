from django.apps import AppConfig

from celery import Celery
from celery.utils.log import get_task_logger
worker_queue = Celery('procedures', broker='amqp://guest@localhost//')


class ProceduresConfig(AppConfig):
    name = 'procedures'
