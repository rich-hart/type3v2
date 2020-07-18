from __future__ import absolute_import, unicode_literals
import celery
import networkx as nx
from django.core.management.base import BaseCommand, CommandError
from neomodel.match import Traversal, OUTGOING , INCOMING , EITHER
from procedures import utils
from django.conf import settings
from celery import Celery
#from project.celery import app as celery_app
from celery.utils.log import get_task_logger
from project.celery import app as celery_app
from procedures.tasks import CTask
from procedures.utils import get_task_plugins

from procedures.models import *

get_task_plugins()

def bfs(root):
    definition = dict(node_class=Queue, direction=OUTGOING,relation_type='DEPENDENCY',model=Dependency)
    visited, queue = dict(), [root]
    while queue:
        vertex = queue.pop(0)
        if vertex.id not in visited:
            visited[vertex.id] = vertex
            relations_traversal = Traversal(vertex,vertex.__label__,definition)
            adj_list = relations_traversal.all()
            current = [v for v in visited.values()]
            next_vertexes = [ a for a in adj_list if a not in current ] 
            queue.extend(next_vertexes)
    return visited

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
   

class Command(BaseCommand):
    help = 'execute procedures'

    def add_arguments(self, parser):
        parser.add_argument('id', type=int)
        parser.add_argument('--type', type=str, default='bucket', help="Object type")
        parser.add_argument('--name', type=str, default='default', help="Procedure name")
        parser.add_argument('--index', type=int, default=0)


    def handle(self, *args, **parameters):
#        import ipdb; ipdb.set_trace()
        
        #FIXME: TODO Only simple default schedule will run
#        worker_queue = Celery(
#            'procedures',
             #broker='amqp://guest@localhost//',
#             broker=settings.CELERY_BROKER_URL,
#             backend=settings.CELERY_RESULT_BACKEND
#        )

        schedule_dict = {}
        procedure = Procedure.get_or_create({"name":parameters['name']})[0]
        schedule = procedure.root.get()
        root = schedule.root.get()
        queues = bfs(root)
        graph = {}

        for id, queue in queues.items():
            #task = queue.task.get()
            #name = utils.Task.__module__ + "." + task.name
            #dependencies = queue.dependencies.all()
            #dependencies = [  utils.Task.__module__ + "." + q.task.get().name for q in dependencies  ]
            #graph[name]=dependencies
            dependencies = queue.dependencies.all()
            graph[id] = [ q.id for q in dependencies ]


        scheduler = Scheduler(graph)
        execution_sequence = scheduler.execution_sequence
        start_queue = queues[execution_sequence[0]]
        start_task = start_queue.task.get()



     
#        start_queue_id = execution_sequence[0]

#        start_queue = queues[start_queue_id]
        #start_queue_name = start_task_name + 
        
#        parameters = {
#            'index': 0
#        }
#        parameters = 1
        #priority = -1
#        parameters = 
#        start_task_name = start_queue.task.get().name
#        start_queue_name = start_task_name + "_" + str(start_queue.id)
        start_args = (parameters.pop('id'),)
        start_signature = celery_app.signature( #send_task
            start_task.name,
            args=start_args,
            kwargs=parameters,
#            options=options,
#            queue=start_queue_name,
#            priority=priority
        )
        linked_tasks = [start_signature]
        for i in range(1,len(execution_sequence)):
            queue_id = execution_sequence[i]
            queue = queues[queue_id]
            task_name = queue.task.get().name
#            queue_name = task_name + "_" + str( queue.id)            

#            task = utils.worker_queue.signature(task_name, queue=queue_name)
            task = celery_app.signature(task_name,kwargs=parameters)
            linked_tasks.append(task)

        signature = celery.chain(linked_tasks)
        import ipdb; ipdb.set_trace()
        result = signature.apply_async()
        #definition = dict(node_class=Task, direction=OUTGOING,
        #          relation_type='END', model=Dependency)
        #relations_traversal = Traversal(root, Task.__label__,
        #                        definition)
        #all_related_queues = relations_traversal.all() 
        #relations = []


#            relations_traversal = Traversal(node,Queue.__label__,definition)
#            schedule_dict[node] = relations_traversal.all()
            
            
#            relations_traversal = Traversal(node,Queue.__label__,definition)
#            dependencies = relations_traversal.all()
           
        
#        tasks = [t for n,t in worker_queue.tasks.items() if Task.__module__ in n]
#        default_schedule = { Task.__module__+ '.' + t: [Task.__module__+ '.'+ n for n in  d ] for t, d in DEFAULT_SCHEDULE.items() }
#        for task in tasks:
#            if task.name not in default_schedule:
#                default_schedule[task.name]=[]
#        scheduler = Scheduler(default_schedule,False)
#
#
#        for task, dependencies in scheduler.dict_of_lists.items():
#            instance = Task.get_or_create({"name": task})[0]
#            for dependency in dependencies:
#                Task.create_or_update({"name": dependency}, relationship=instance.dependencies)
#bobs_gizmo = Dog.get_or_create({"name": "Gizmo"}, relationship=bob.pets)
#            Task.create_or_update(



#        tasks = [{"name":name} for name in worker_queue.tasks if Task.__module__ in name ]
#        tasks = Task.create_or_update(*tasks)
#        task_dict = { task.name: task for task in tasks } 
#        for task in tasks:
#            basename = task.name.replace(Task.__module__ + '.','')
#            for dependency in DEFAULT_SCHEDULE.get(basename,[]):
#                dependency = Task.__module__ + '.' + dependency
#                dependency = task_dict[dependency]
#                task.dependencies.connect(dependency)
            #task.save()
#        for name in worker_queue.tasks:
#            if Task.__module__ in name:
#                tasks[name] =  Task.create_or_update({'name':name})
#        for name, parents in SCHEDULES.items():
#            name = Task.__module__ + "." + name
#            task = tasks[name]
#            for parent in parents:
#                parent = Task.__module__ + "." + parent
#                dependency = tasks[parent]
#                task.dependencies.connect(dependency)
#        job_id = options['job_id']
#        synchronous = options['synchronous']
#        if synchronous:
#            start(job_id)
#        else:
#            thread = threading.Thread(target=start,args=(job_id,))
#            thread.start()

#        job = Job.objects.get(pk=job_id)

