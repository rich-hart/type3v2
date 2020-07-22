from django.urls import path, include
from rest_framework import routers


from .views import *

router = routers.DefaultRouter()
#router.register('classifications', ClassificationViewSet)

router.register(r'files', FileViewSet)
router.register(r'buckets', BucketViewSet)
router.register(r'fsobjects', FSObjectViewSet)

urlpatterns = [
    # ex: /jobs/
    path('', include((router.urls,'buckets'),namespace='buckets')),
]

