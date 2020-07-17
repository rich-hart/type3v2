import networkx as nx
from django.core.management.base import BaseCommand, CommandError
from neomodel.match import Traversal, OUTGOING , INCOMING , EITHER
from procedures.models import *


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
    

class Command(BaseCommand):
    help = 'execute procedures'

    def add_arguments(self, parser):
        parser.add_argument('--name', type=str,default='default')

    def handle(self, *args, **options):
        #FIXME: TODO Only simple default schedule will run
        import ipdb; ipdb.set_trace()
        schedule_dict = {}
        procedure = Procedure.get_or_create({"name":options['name']})[0]
        schedule = procedure.root.get()
        root = schedule.root.get()
        queues = bfs(root)
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

