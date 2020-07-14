from django.shortcuts import render

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from bases.views import IsOwner
from django.core.management import call_command

from .models import *
from .serializers import *

class JobViewSet(viewsets.ModelViewSet):
    queryset = Job.objects.all()
    serializer_class = JobSerializer

    def perform_create(self, serializer):
        #FIXME: create profile in user view when merged
        serializer.save(owner=self.request.user.profile, status=Job.Status.CREATED.value)
        

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

class ClassificationViewSet(JobViewSet):
    queryset = Classification.objects.all()
    serializer_class = ClassificationSerializer

    def perform_create(self, serializer):
        #FIXME: create profile in user view when merged
        instance = serializer.save(owner=self.request.user.profile, status=Job.Status.CREATED.value)
        for user in User.objects.all():
            assignee = Assignee.objects.create(profile=user.profile, job=instance)


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
