from django.core.management.base import BaseCommand, CommandError
from procedures.models import *

#import threading


#def start(job_id):
#    """thread worker function"""
#    job = Job.objects.get(pk=job_id)
#    job.run()


class Command(BaseCommand):
    help = 'load procedures into neo4j db'

#    def add_arguments(self, parser):
#        parser.add_argument('job_id', type=int)
#        parser.add_argument('--synchronous', type=bool, default=True)

    def handle(self, *args, **options):

        for name in worker_queue.tasks:
            if Task.__module__ in name:
                Task.create_or_update({'name':name})
                #Task.get_or_create({'name':'test1asd'}) 
                pass
        
#        job_id = options['job_id']
#        synchronous = options['synchronous']
#        if synchronous:
#            start(job_id)
#        else:
#            thread = threading.Thread(target=start,args=(job_id,))
#            thread.start()

#        job = Job.objects.get(pk=job_id)

