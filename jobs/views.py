from django.shortcuts import render

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from bases.views import IsOwner
from django.core.management import call_command
from procedures.utils import process 
from django.contrib.auth.models import User, Group, AnonymousUser
from buckets.models import File

from procedures.tasks import copy as copy_file

from .models import *
from .serializers import *

class JobViewSet(viewsets.ModelViewSet):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    STAGING_SIZE = 20
#    def get_queryset(self):
#        user = self.request.user
#        if isinstance(user, AnonymousUser):
#            return []
#        Assignee.
#        return Job.objects.filter(owner=user.profile)

    def perform_create(self, serializer):
        instance = serializer.save(
            owner=self.request.user.profile,
            status=Job.Status.CREATED.value,
        )
        call_command('start', instance.id)
        
    @action(
        detail=True,
        methods=['GET', 'PATCH'],
#        methods=['PATCH','patch','post'],
#        permission_classes=[IsOwner],
    )
    def start(self, request, pk):
        job = Job.objects.get(pk=pk)
        call_command('start',pk)
        data = {'status':job.status}
        return Response(data)    

    @action(
        detail=True,
        methods=['GET','POST'],
    )
    def perform(self, request, pk):
        import ipdb; ipdb.set_trace()
        instance = self.get_object()
        queue = Queue(instance.queue_name,inactivity_timeout=.3)

        if 'staging_queue' not in request.session:
            request.session['staging_queue'] = []

        while len(request.session['staging_queue']) <= self.STAGING_SIZE:
            item = queue.get()
            if not item:
                break
            request.session['staging_queue'].append(item)

        for tag in request.session['staging_queue']:
            file = File.objects.get(tag=tag)
            copy_file.delay([file.id])          

        

        data = {
            "msg": None
        }
        return Response(data) 


#class ClassificationViewSet(JobViewSet):
#    queryset = Classification.objects.all()
#    serializer_class = ClassificationSerializer
#
#    def perform_create(self, serializer):
#        #FIXME: create profile in user view when merged
#        import ipdb; ipdb.set_trace()
#
#        instance = serializer.save(owner=self.request.user.profile, status=Job.Status.CREATED.value)
#        for user in User.objects.all():
#            assignee = Assignee.objects.create(profile=user.profile, job=instance)
#
#    @action(
#        detail=True,
#        methods=['GET', 'PATCH'],
##        methods=['PATCH','patch','post'],
##        permission_classes=[IsOwner],
#    )
#    def start(self, request, pk):
#        job = Job.objects.get(pk=pk)
#        call_command('start',pk)
#        data = {'status':job.status}
#        return Response(data)
