import os

from contextlib import ContextDecorator
import json

import pika
from pika.exceptions import ChannelClosedByBroker


from django.conf import settings

#from .apps import worker_queue, get_task_logger

#FIXME: Refactor queue, utils, and tasks.  
#  new import should be ( merge queue into utils, utils --> tasks)

# See methods at https://docs.python.org/3/library/queue.html
class BaseQueue(ContextDecorator):
    def __enter__(self):
        return self

    def __exit__(self, *exc):
        return False

    def qsize(self, *args):
        raise NotImplementedError
    def empty(self, *args):
        raise NotImplementedError
    def full(self, *args):
        raise NotImplementedError
    def put(self, *args):
        raise NotImplementedError
    def put_nowait(self, *args):
        raise NotImplementedError
    def get(self, *args):
        raise NotImplementedError
    def task_done(self, *args):
        raise NotImplementedError
    def join(self, *args):
        raise NotImplementedError
    def __iter__(self):
        return self

    def __next__(self):
        raise NotImplementedError

class Queue(BaseQueue):
    def __init__(self, name, server_url, *args,**kwargs):
        self.name = name
        self.server_url = server_url
        super(Queue,self).__init__(*args)


class RabbitMQ(Queue):
    _connection = None
    _channel = None

    def __init__(
            self,
            name='',
            server_url=settings.MESSAGE_QUEUE_HOST,
            exclusive=False,
            no_ack=True,
            auto_ack_consumer=True,
            auto_delete=False,
            durable=True,
            inactivity_timeout=None,
        ):
        super(RabbitMQ, self).__init__(name,server_url)
        self.auto_ack_consumer=auto_ack_consumer
        self.inactivity_timeout=inactivity_timeout
        self.server_url = server_url
        if self.name:
            self.channel.queue_declare(
                queue=self.name, durable=durable,
                exclusive=exclusive, auto_delete=auto_delete,
            )

    @classmethod
    def create(cls,*args,**kwargs):
        #create queue and disconnect immediately
        cls(*args,**kwargs).disconnect() 

    @staticmethod
    def delete(
           name,
           server_url=settings.MESSAGE_QUEUE_HOST,
           **kwargs,
        ):
        #create queue and disconnect immediately
        connection = pika.BlockingConnection(
            pika.URLParameters(server_url)
        )
        channel = connection.channel()
        channel.queue_delete(name,**kwargs)
        channel.close()
        connection.close()

    @staticmethod
    def exists(name, server_url=settings.MESSAGE_QUEUE_HOST, **kwargs):
        connection = pika.BlockingConnection(
            pika.URLParameters(server_url)
        )
        channel = connection.channel()
        try:
            result = bool(channel.queue_declare(name, passive=True,**kwargs))
        except ChannelClosedByBroker:
            result = False

        channel.close() if channel.is_open else 0
        connection.close() if connection.is_open else 0
        return result

    @property
    def connection(self):
        if self._connection is None or self._connection.is_closed:
            self._connection = pika.BlockingConnection(
                pika.URLParameters(self.server_url)
            )
        return self._connection

    @property
    def channel(self):
        if self._channel is None or self._channel.is_closed:
            self._channel = self.connection.channel()
        return self._channel

    def qsize(self):
        queue_proxy = self.channel.queue_declare(
            queue=self.name, durable=True,
            exclusive=False, auto_delete=False, passive=True
        )
        size = queue_proxy.method.message_count
        return size

    def empty(self):
        return self.qsize() == 0

    def put(self, item, exchange=''):
        self.channel.basic_publish(exchange=exchange,
                  routing_key=self.name,
                  body=json.dumps(item),
                  properties=pika.BasicProperties(
                     delivery_mode = 2, # make message persistent
        ))

    def get(self):
        item = self.__next__()
        return item

    def __next__(self):
        _, _, body = next(self.channel.consume(self.name,auto_ack=self.auto_ack_consumer,inactivity_timeout=self.inactivity_timeout))
        item = json.loads(body) if body else None
        return item

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        if self._channel is None and self._channel.is_open:
            self._channel.close()
        return False

    def disconnect(self):
        if self._channel is None and self._channel.is_open:
            self._channel.close()
        if self._connection is None and self._connection.is_open:
            self._connection.close()

