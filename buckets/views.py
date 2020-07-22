from django.shortcuts import render

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.models import User, Group, AnonymousUser
from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer, TemplateHTMLRenderer

from .models import *
from .serializers import *

class PDF_Renderer(BrowsableAPIRenderer):
    format = 'pdf'
    template = 'pdf.html'

class FSObjectViewSet(viewsets.ModelViewSet):
    queryset = FSObject.objects.all()
    serializer_class = FSObjectSerializer


class BucketViewSet(viewsets.ModelViewSet):
    queryset = Bucket.objects.all()
    serializer_class = BucketSerializer

class FileViewSet(viewsets.ModelViewSet):
    queryset = File.objects.all()
    serializer_class = FileSerializer 

    @action(
        detail=True,
        renderer_classes=[
            PDF_Renderer,
        ]
    )
    def render(self, request, pk):
#        import ipdb; ipdb.set_trace()
        return Response({})

