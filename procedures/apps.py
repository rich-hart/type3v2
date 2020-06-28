from django.apps import AppConfig

from celery import Celery

worker_queue = Celery('procedures', broker='amqp://guest@localhost//')


class ProceduresConfig(AppConfig):
    name = 'procedures'
