from django.db import models
from neomodel import StructuredNode, StringProperty, StructuredRel, RelationshipTo, ZeroOrOne, IntegerProperty, ZeroOrMore, One, RelationshipFrom
#from project.celery import app as celery_app, get_task_logger
from networkx import nx
import celery
from .apps import worker_queue, get_task_logger 


class Dependency(StructuredRel):
#    since = DateTimeProperty(
#        default=lambda: datetime.now(pytz.utc)
#    )
    TYPES = {'S': 'Schedule', 'P': 'Procedure'}
    type = StringProperty(required=True, choices=TYPES)
    id = IntegerProperty(required=True)

class Task(StructuredNode):
    name = StringProperty(unique_index=True)

class Queue(StructuredNode):
    task = RelationshipTo('Task', 'task')
    dependencies = RelationshipTo('Queue', 'DEPENDENCY', cardinality=ZeroOrMore, model=Dependency)

class Schedule(StructuredNode):
    name = StringProperty(unique_index=True)
    root = RelationshipFrom('Queue', 'END', cardinality=One)

class Procedure(StructuredNode):
    name = StringProperty(unique_index=True)
    root = RelationshipFrom('Queue', 'TERMINATE', cardinality=One)


#    dependencies = RelationshipTo('Procedure', 'DEPENDENCY', cardinality=ZeroOrMore, model=Dependency)

#    root = RelationshipTo('Schedule', 'END', cardinality=ZeroOrOne)

#    root = RelationshipTo('Task', 'END', cardinality=One)

#class ScheduleRelation(StructuredRel):
#    index = IntegerProperty()




DEFAULT_PROCEDURE = {
    'default': [],
}

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






#DEFAULT_SCHEDULE = {
#  'end': ['start'],
#}

#DEFAULT_PROCEDURE = [
#  DEFAULT_SCHEDULE,
#]

#TODO  Move to utils
class Scheduler(nx.DiGraph):
    _execution_sequence = None

    @property
    def execution_sequence(self):
        if not self._execution_sequence:
            self._execution_sequence = list(nx.algorithms.dag.topological_sort(self))
        return self._execution_sequence

    @property
    def dict_of_lists(self):
        return nx.convert.to_dict_of_lists(self)

    def __init__(self, dependencies=None, reverse=True, name='default'):

        if reverse:
            dependency_graph = nx.DiGraph(dependencies)
            execution_graph = dependency_graph.reverse(copy=False)
            executions = nx.convert.to_dict_of_lists(execution_graph)
        else:
            executions = dependencies
        super(Scheduler, self).__init__(executions)
        self.name = name
#        Task.create
#NOTE: https://docs.celeryproject.org/en/stable/userguide/tasks.html#names
#>>> @app.task(name='sum-of-two-numbers')
#>>> def add(x, y):
#...     return x + y

#>>> add.name
#'sum-of-two-numbers'
