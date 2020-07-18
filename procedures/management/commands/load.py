from __future__ import absolute_import, unicode_literals
import networkx as nx
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
#from project.celery import app as celery_app
from project.celery import app as celery_app
from procedures import utils
from procedures.models import *
#from procedures.tasks import *

#import threading


#def start(job_id):
#    """thread worker function"""
#    job = Job.objects.get(pk=job_id)
#    job.run()

utils.get_task_plugins()

class Command(BaseCommand):
    help = 'load procedures into neo4j db'


    def handle(self, *args, **options):

        procedure = Procedure.create({"name": 'default'})[0]

        procedures = {}
        schedules = {}
#        tasks = {
#            n.replace(CTask.__module__ + '.','') : t 
#              for n,t in celery_app.tasks.items() 
#                if CTask.__module__ in n
#        }
        tasks = celery_app.tasks 
        for name in tasks:
            tasks[name] = Task.get_or_create({"name": name})[0]
#            tasks[name] = Task.get_or_create({"name": name})[0]

#        begin = tasks['procedures.tasks.begin']
#        execute = tasks['procedures.tasks.execute']

#        p_scheduler = Scheduler(utils.DEFAULT_PROCEDURE,False)
#        procedure = Procedure.get_or_create({"name": p_scheduler.name})[0]


        scheduler = Scheduler(utils.DEFAULT_SCHEDULE,False)
        schedule = Schedule.create({"name": scheduler.name})[0]

        import ipdb; ipdb.set_trace()
        start_node = 'procedures.tasks.begin'
        first_nodes = {n for n, d in scheduler.dict_of_lists.items() if not d }
#        scheduler.add_edges_from(*zip(first_nodes,len(first_nodes)*['start']))
#        edges = [ e for e in zip(first_nodes,len(first_nodes)*[start_node])]
        first_edges = list(zip(first_nodes,len(first_nodes)*[start_node]))
#        scheduler.add_edges_from(list(zip(first_nodes,len(first_nodes)*[start_node]))) 
        scheduler.add_edges_from(first_edges)

        execution_graph = scheduler.reverse()

        last_nodes = [x for x in execution_graph.nodes() if execution_graph.out_degree(x)==0 and execution_graph.in_degree(x)==1]

        stop_node = 'procedures.tasks.stop'

        last_edges = list(zip(len(last_nodes)*[stop_node],last_nodes))
        scheduler.add_edges_from(last_edges)

#        scheduler.add_node('procedures.tasks.end')
#        scheduler.add_node('procedures.tasks.begin')

#        nodes = [ n for n in scheduler.nodes] 


#        scheduler.add_node('end')
#        scheduler.add_node('begin')

        queues = {} 

       

        for name in scheduler.nodes:
            task = tasks[name]
            queue = Queue().save()
            queue.task.connect(task)
            queue.save()
            queues[name] = queue
       
        #END TASK
#        for n1,n2 in zip(['end']*len(nodes),nodes):
#            scheduler.add_edge(n1,n2)
        #Begin Task
#        for n1,n2 in zip(['begin']*len(nodes),nodes):
#            scheduler.add_edge(n2,n1)
      
        for name, dependencies in scheduler.dict_of_lists.items():
            queue = queues[name]
            for name in dependencies:
                dependency = queues[name]
                queue.dependencies.connect(dependency,{'type':'S','id':schedule.id})


                
        last = scheduler.execution_sequence[0]
        last = queues[last]

        schedule.root.connect(last)
        schedule.save()
#        terminate = tasks['terminate']
#        terminate = Queue(task=terminate).save()
#        terminate.dependencies.connect(end, {'type':'P','id':procedure.id})
        procedure.root.connect(schedule)
        procedure.save()

        for queue in queues.values():
            queue.save()
#            dependencies = [ {"task": tasks[n] } for n in dependencies ]
                        
#            queues[name] = Queue.create_or_update(dependencies, relationship=queue.dependencies)[0]
              
#            for name in dependencies:
#                dependency = queues[name]
#                task = tasks[name]
#                queue = Queue.create_or_update({"task":task}, relationship=queue.dependencies)[0]
                #Queue.create_or_update({"task": dependency}, relationship=queue.dependencies)
                #queue.dependencies.connect(dependency,{'type':'S','id':schedule.id})
#            queue.save()
#        for _,queue in queues.items():
#            queue.save() 
                #task = Task.create_or_update(
                #    [{"name": dependency}],
                #    relationship=instance.dependencies,
                    #{'type': 'S', 'id': schedule.id}
                #)
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

