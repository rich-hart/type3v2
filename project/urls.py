"""type3 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
from django.urls import path, include

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import routers

@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'files': reverse('file-list', request=request, format=format),
        'buckets': reverse('bucket-list', request=request, format=format),

#        'snippets': reverse('snippet-list', request=request, format=format)
    })

from jobs.views import JobViewSet
from buckets.views import BucketViewSet, FileViewSet, FSObjectViewSet
router = routers.DefaultRouter()

router.register(r'jobs', JobViewSet,basename='job')
router.register(r'files', FileViewSet)
router.register(r'buckets', BucketViewSet)
router.register(r'fsobjects', FSObjectViewSet)
urlpatterns = [
    path('admin/', admin.site.urls),
#    path('jobs/', include('jobs.urls')),
    path('api/', include(router.urls)),
#    path('classifiers/', include('jobs.urls')),
#    path('api/buckets/', include('buckets.urls'), name='buckets-root'),
#    path('api/buckets/', include(('buckets.urls','buckets'),namespace='bucket')),
#    path('api/jobs/', include(('jobs.urls', 'jobs'),namespace='project-jobs')),
#    path('api/', api_root, name='project-api'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]

#if settings.DEBUG:
#    urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

