from django.shortcuts import render

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from bases.views import IsOwner
from .models import *
from .serializers import *

class JobViewSet(viewsets.ModelViewSet):
    queryset = Job.objects.all()
    serializer_class = JobSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user.profile,status=Job.Status.CREATED.value)

    @action(
        detail=True,
        #methods=['get'],
        permission_classes=[IsOwner],
    )
    def start(self, request, pk):
        data = {}
        return Response(data)    

