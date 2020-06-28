from .apps import worker_queue


@worker_queue.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))

