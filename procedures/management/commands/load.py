import networkx as nx
from django.core.management.base import BaseCommand, CommandError
from procedures.models import *

#import threading


#def start(job_id):
#    """thread worker function"""
#    job = Job.objects.get(pk=job_id)
#    job.run()

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

    def __init__(self, dependencies=None, reverse=True):
        if reverse:
            dependency_graph = nx.DiGraph(dependencies)
            execution_graph = dependency_graph.reverse(copy=False)
            executions = nx.convert.to_dict_of_lists(execution_graph)
        else:
            executions = dependencies
        super(Scheduler, self).__init__(executions)

class Command(BaseCommand):
    help = 'load procedures into neo4j db'

#    def add_arguments(self, parser):
#        parser.add_argument('job_id', type=int)
#        parser.add_argument('--synchronous', type=bool, default=True)

    def handle(self, *args, **options):
        import ipdb; ipdb.set_trace()
#        schedule = { n: t for n, t in worker_queue.tasks.items() if Task.__module__ in n }
#        tasks = [worker_queue.tasks.items() if Task.__module__ in n]
        tasks = [t for n,t in worker_queue.tasks.items() if Task.__module__ in n]
        default_schedule = { Task.__module__+ '.' + t: [Task.__module__+ '.'+ n for n in  d ] for t, d in DEFAULT_SCHEDULE.items() }
        for task in tasks:
            if task.name not in default_schedule:
                default_schedule[task.name]=[]
        scheduler = Scheduler(default_schedule,False)


        for task, dependencies in scheduler.dict_of_lists.items():
            instance = Task.get_or_create({"name": task})[0]
            for dependency in dependencies:
                Task.create_or_update({"name": dependency}, relationship=instance.dependencies)
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

