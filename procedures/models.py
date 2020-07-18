from django.db import models
from neomodel import (
    StructuredNode, StringProperty, StructuredRel,
     RelationshipTo, ZeroOrOne, IntegerProperty, ZeroOrMore, One, RelationshipFrom
)
from networkx import nx


class Dependency(StructuredRel):
    TYPES = {'S': 'Schedule', 'P': 'Procedure'}
    type = StringProperty(required=True, choices=TYPES)
    id = IntegerProperty(required=True)

class Task(StructuredNode):
    name = StringProperty(unique_index=True)

class Queue(StructuredNode):
    task = RelationshipTo('Task', 'TASK', cardinality=One)
    dependencies = RelationshipTo('Queue', 'DEPENDENCY', cardinality=ZeroOrMore, model=Dependency)

class Schedule(StructuredNode):
    name = StringProperty(unique_index=True)
    root = RelationshipTo('Queue', 'END', cardinality=One)

class Procedure(StructuredNode):
    name = StringProperty(unique_index=True)
    root = RelationshipTo('Schedule', 'TERMINATE', cardinality=One)



# NOTE: Tools and procedures should be defined last. 
# Create your models here.

# NOTE: Mabye always pass array of objects but only process one. 

# class Procedure # is many schedules 

#NOTE: https://docs.celeryproject.org/en/stable/userguide/tasks.html#bound-tasks

#logger = get_task_logger(__name__)

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

#    def execute(self, parameters, synchronous=False, options=None):
#        start_task_name = self._execution_sequence[0]
#        priority=10
#        queue = 'celery' if self._queue_type == 'celery' else QUEUE_MAP[start_task_name]
#        logger.info(f"queue: {queue}")
#
#        start_task = celery_app.signature(
#            start_task_name,
#            args=(parameters,),
#            options=options,
#            queue=queue,
#            priority=priority
#        )
#        linked_tasks = [start_task]
#        priority -= 1
#        for i in range(1,len(self._execution_sequence)):
#            task_name = self._execution_sequence[i]
#            queue = 'celery' if self._queue_type == 'celery' else QUEUE_MAP[task_name]
#
#            task = celery_app.signature(task_name, queue=queue, priority=priority)
#            linked_tasks.append(task)
#            priority -= 1
#        if synchronous:
#            linked_tasks[0].args=tuple()
#            for task in linked_tasks:
#                task=celery_app.tasks[task.name]
#                results = task(parameters)
#                task.on_success()
#                parameters = results
#        else:
#            chain(linked_tasks).apply_async()
#        Task.create
#NOTE: https://docs.celeryproject.org/en/stable/userguide/tasks.html#names
#>>> @app.task(name='sum-of-two-numbers')
#>>> def add(x, y):
#...     return x + y

#>>> add.name
#'sum-of-two-numbers'
