from django.urls import path, include
from rest_framework import routers


from .views import *

router = routers.DefaultRouter()
router.register('',BinaryClassifierViewSet,basename='classifier')


urlpatterns = [
    # ex: /jobs/
    path('', include(router.urls)),
]

