from django.core.management.base import BaseCommand, CommandError
from jobs.models import Job

import threading


def run(job_id):
    """thread worker function"""
    job = Job.objects.get(pk=job_id)
    job = getattr(job,'classification',job)
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
            run(job_id)
        else:
            thread = threading.Thread(target=run,args=(job_id,))
            thread.start()

#        job = Job.objects.get(pk=job_id)

