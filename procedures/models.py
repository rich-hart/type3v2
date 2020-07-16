from django.db import models
from neomodel import StructuredNode, StringProperty, StructuredRel, RelationshipTo
#from project.celery import app as celery_app, get_task_logger

import celery
from .apps import worker_queue, get_task_logger 


#class Dependency(StructuredRel):
#    pass
#    since = DateTimeProperty(
#        default=lambda: datetime.now(pytz.utc)
#    )
#    met = StringProperty()

class Task(StructuredNode):
    name = StringProperty(unique_index=True)
    dependencies = RelationshipTo('Task', 'DEPENDENCY')
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

@worker_queue.task(bind=True)
def add(self, x, y):
    logger.info(self.request.id)

class MyTask(celery.Task):

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        print('{0!r} failed: {1!r}'.format(task_id, exc))

@worker_queue.task(base=MyTask)
def my_add(x, y):
    raise KeyError()

@worker_queue.task
def start(*args):
    return args

@worker_queue.task
def end(*args):
    return args


DEFAULT_SCHEDULE = {
   'end' : ['start']
}

#        Task.create
#NOTE: https://docs.celeryproject.org/en/stable/userguide/tasks.html#names
#>>> @app.task(name='sum-of-two-numbers')
#>>> def add(x, y):
#...     return x + y

#>>> add.name
#'sum-of-two-numbers'
