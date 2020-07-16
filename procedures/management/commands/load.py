import networkx as nx
from django.core.management.base import BaseCommand, CommandError
from procedures import utils
from procedures.models import *

#import threading


#def start(job_id):
#    """thread worker function"""
#    job = Job.objects.get(pk=job_id)
#    job.run()


class Command(BaseCommand):
    help = 'load procedures into neo4j db'


    def handle(self, *args, **options):
        import ipdb; ipdb.set_trace()
        procedure = Procedure.get_or_create({"name": 'default'})[0]

        procedures = {}
        schedules = {}
        tasks = {
            n.replace(utils.Task.__module__ + '.','') : t 
              for n,t in utils.worker_queue.tasks.items() 
                if utils.Task.__module__ in n
        }
        
        for name in tasks:
            tasks[name] = Task.get_or_create({"name": name})[0]

        begin = tasks['begin']
        end = tasks['end']
        execute = tasks['execute']
        terminate = tasks['terminate']

#        p_scheduler = Scheduler(utils.DEFAULT_PROCEDURE,False)
#        procedure = Procedure.get_or_create({"name": p_scheduler.name})[0]


        scheduler = Scheduler(utils.DEFAULT_SCHEDULE,False)
        schedule = Schedule.get_or_create({"name": scheduler.name})[0]

        nodes = [ n for n in scheduler.nodes] 


        scheduler.add_node('end')
        scheduler.add_node('begin')

        queues = {} 

       

        for name in scheduler.nodes:
            task = tasks[name]
            queues[name] = Queue(task=task).save()
       
        #END TASK
        for n1,n2 in zip(['end']*len(nodes),nodes):
            scheduler.add_edge(n1,n2)
        #Begin Task
        for n1,n2 in zip(['begin']*len(nodes),nodes):
            scheduler.add_edge(n2,n1)
      
        for name, dependencies in scheduler.dict_of_lists.items():
            queue = queues[name]
            for name in dependencies:
                dependency = queues[name]
                queue.dependencies.connect(dependency,{'type':'S','id':schedule.id})                
        
        end = queues['end']
        schedule.root.connect(end)
        terminate = tasks['terminate']
        terminate = Queue(task=terminate).save()
        terminate.dependencies.connect(end, {'type':'P','id':procedure.id})
        procedure.root.connect(terminate)
        procedure.save()

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

