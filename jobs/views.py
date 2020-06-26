from django.shortcuts import render

from rest_framework import viewsets

from .models import *
from .serializers import *

class JobViewSet(viewsets.ModelViewSet):
    queryset = Job.objects.all()
    serializer_class = JobSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user.profile,status=Job.Status.CREATED.value)
