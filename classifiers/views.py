from django.shortcuts import render

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from bases.views import IsOwner
from django.core.management import call_command

from .models import *
from .serializers import *

#class BinaryClassifierViewSet(viewsets.ModelViewSet):
#    queryset = Classifier.objects.all() #try to keep base queryset when possible, query with string instread . 
#    serializer_class = BinaryClassifierSerializer
#    # FIXME: TODO filter query for human classifier
#    def perform_update(self, serializer):
#        #serializer.save(owner=self.request.user.profile,status=Job.Status.CREATED.value)
#        pass 
#
