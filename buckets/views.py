from django.shortcuts import render

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.models import User, Group, AnonymousUser
from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer, TemplateHTMLRenderer
from rest_framework.pagination import PageNumberPagination
import django_filters
from django.shortcuts import redirect
from django.urls import reverse
from .models import *
from .serializers import *


class PDF_Renderer(BrowsableAPIRenderer):
    format = 'pdf'
    template = 'pdf.html'

class FileResultsSetPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100

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
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = ['parent']
    pagination_class=FileResultsSetPagination
    renderer_classes=[
        BrowsableAPIRenderer,
        JSONRenderer,
        PDF_Renderer,
    ]

#    @action(
#        detail=False,
#        methods=['GET'],
#        renderer_classes=[
#            BrowsableAPIRenderer,
#            JSONRenderer,
#            PDF_Renderer,
#        ],
#        filter_backends = [django_filters.rest_framework.DjangoFilterBackend],
#        filterset_fields = ['parent'],

#        methods=['PATCH','patch','post'],
#        permission_classes=[IsOwner],
#    )
#    def render(self, request,*args,**kwargs):
#        job = Job.objects.get(pk=pk)
#        call_command('start',pk)
        #data = {}
        #response = super(FileViewSet, self).as_view
        #url = reverse
#        return redirect('file-list')   

#    def get(self, request, pk=None):
  
#        import ipdb; ipdb.set_trace()


#        pagination_class = SingleResultsSetPagination,
