from django.urls import path, include
from rest_framework import routers


from .views import *

router = routers.DefaultRouter()
#router.register('classifications', ClassificationViewSet)

router.register('jobs', JobViewSet,basename='job')
#router.register('', ClassificationViewSet)

urlpatterns = [
    # ex: /jobs/
    path('', include(router.urls)),
]

