from django.db import models
from neomodel import StructuredNode, StringProperty
from project.celery import app as celery_app, get_task_logger
import celery

class Task(StructuredNode):
    name = StringProperty(unique_index=True)

# NOTE: Tools and procedures should be defined last. 
# Create your models here.

# NOTE: Mabye always pass array of objects but only process one. 

# class Task(Neo4j)
# class Schedule

# In celery task passing if objects of list returned, append it to the 
# message objects ( should be a set of object tag hashes) Maybe with model name dict instead of set?. 
# Try to use celery groups for task Many to Many relationships

# class Procedure # is many schedules 

#NOTE: https://docs.celeryproject.org/en/stable/userguide/tasks.html#bound-tasks
logger = get_task_logger(__name__)

#A task being bound means the first argument to the task will always be the task instance (self), just like Python bound methods:

@celery_app.task(bind=True)
def add(self, x, y):
    logger.info(self.request.id)

class MyTask(celery.Task):

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        print('{0!r} failed: {1!r}'.format(task_id, exc))

@celery_app.task(base=MyTask)
def my_add(x, y):
    raise KeyError()


#NOTE: https://docs.celeryproject.org/en/stable/userguide/tasks.html#names
#>>> @app.task(name='sum-of-two-numbers')
#>>> def add(x, y):
#...     return x + y

#>>> add.name
#'sum-of-two-numbers'
