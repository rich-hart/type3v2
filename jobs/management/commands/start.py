from django.core.management.base import BaseCommand, CommandError
from jobs.models import Job

import threading


def worker(job_id):
    """thread worker function"""
    job = Job.objects.get(job_id)
    job.run()


class Command(BaseCommand):
    help = 'Start job'

    def add_arguments(self, parser):
        parser.add_argument('job_id', type=int)

    def handle(self, *args, **options):
        job_id = options['poll_ids']
        thread = threading.Thread(target=worker,args=(job_id,))
        thread.start()

