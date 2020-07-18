from __future__ import absolute_import, unicode_literals
import celery
import networkx as nx
from django.core.management.base import BaseCommand, CommandError
from neomodel.match import Traversal, OUTGOING , INCOMING , EITHER
from procedures import utils
from django.conf import settings
from celery import Celery
#from project.celery import app as celery_app
from celery.utils.log import get_task_logger
from project.celery import app as celery_app
from procedures.tasks import CTask
from procedures.utils import get_task_plugins
from neomodel import db

from procedures.models import *

get_task_plugins()

def deleteData():
    query = 'MATCH (n) DETACH DELETE n'
    db.cypher_query(query)


class Command(BaseCommand):
    help = 'execute procedures'

    def add_arguments(self, parser):
        parser.add_argument('-f','--force', action='store_true')

    def handle(self, *args, **parameters):
        if not parameters['force']:
            print('\n'*10)
            response = input("Are you sure? [yes]\nThis cannot be undone!\n"+'\n'*5)

            if 'yes' not in response.lower():
                self.stdout.write(self.style.SUCCESS('Cancelled'))
                return 
        deleteData()
        self.stdout.write(self.style.SUCCESS('Deleted procedures'))

