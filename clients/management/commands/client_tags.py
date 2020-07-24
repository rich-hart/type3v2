import os
import argparse
import yaml

try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper
    yaml.Loader = Loader

from django.core.management.base import BaseCommand, CommandError
from project.models import Tag, ProjectTag, Mongo
from clients.models import BusinessClient

class Command(BaseCommand):
    help = 'load tags'

    def add_arguments(self, parser):
        parser.add_argument('paths', nargs='+', type=argparse.FileType('r'))

    def handle(self, *args, **options):
        import ipdb; ipdb.set_trace()
        mongo = Mongo()
        collection = mongo.db[BusinessClient.__class__.__name__]
        for path in options['paths']:
            filename = os.path.basename(path.name)
            tag_id = filename.split(os.extsep)[0]
            client, client_created = BusinessClient.objects.get_or_create(tag=tag_id)
            data = yaml.load(path, Loader=yaml.Loader)
            if client_created:
                tag = ProjectTag.objects.create(id=tag_id,_data=data)
            else:
                tag = ProjectTag.objects.get(id=tag_id)
 
#            tag, tag_created = ProjectTag.objects.get_or_create(id=tag_id,_data=data)
            Tag.objects.update_tags(client, tag_id)

#            tag_data = [ d for d in collection.find({"_id":clienttag.id}) ] #FIXME: better update?
#            if tag_created:
#                collection.insert_one(data)   

