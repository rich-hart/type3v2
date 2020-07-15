from django.urls import path, include
from rest_framework import routers


from .views import *

router = routers.DefaultRouter()
router.register('',JobViewSet)
#router.register('classifications',ClassificationViewSet)


urlpatterns = [
    # ex: /jobs/
    path('', include(router.urls)),
]

