from django.core.management.base import BaseCommand, CommandError
from jobs.models import Job

import threading


def start(job_id):
    """thread worker function"""
    job = Job.objects.get(pk=job_id)
    job.run()


class Command(BaseCommand):
    help = 'Start job'

    def add_arguments(self, parser):
        parser.add_argument('job_id', type=int)
        parser.add_argument('--synchronous', type=bool, default=True)

    def handle(self, *args, **options):
        job_id = options['job_id']
        synchronous = options['synchronous']
        if synchronous:
            start(job_id)
        else:
            thread = threading.Thread(target=start,args=(job_id,))
            thread.start()

#        job = Job.objects.get(pk=job_id)

