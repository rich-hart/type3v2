from django.shortcuts import render

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from bases.views import IsOwner
from django.core.management import call_command
from django.contrib.auth.models import User, Group, AnonymousUser

from .models import *
from .serializers import *

class BinaryClassifierViewSet(viewsets.ModelViewSet):
#    queryset = Classifier.objects.all().order_by("?") #try to keep base queryset when possible, query with string instread . 
    serializer_class = BinaryClassifierSerializer
    # FIXME: TODO filter query for human classifier
    def get_queryset(self):
        user = self.request.user
        if isinstance(user, AnonymousUser):
            return []
        return Human.objects.filter(profile=user.profile)

    def perform_create(self, serializer):
        #serializer.save(owner=self.request.user.profile,status=Job.Status.CREATED.value)
        pass 


    def perform_update(self, serializer):
        #serializer.save(owner=self.request.user.profile,status=Job.Status.CREATED.value)
        pass 

