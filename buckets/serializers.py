from rest_framework import serializers

from .models import *

class FileSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = File
        fields = (
            'id',
            'url',
            'format',
#            'instance',
        )
        read_only_fields = fields
#        extra_kwargs = {
#            'url': {'view_name': 'buckets:file','lookup_field': 'pk'}
#        }

class BucketSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Bucket
        fields = (
            'id',
            'url',
        )
        read_only_fields = fields
#        extra_kwargs = {
#            'url': {'view_name': 'buckets:bucket', 'lookup_field': 'pk'}
#        }
class FSObjectSerializer(serializers.HyperlinkedModelSerializer):
    bucket = BucketSerializer(read_only=True)
    file = FileSerializer(read_only=True)
    root = serializers.HyperlinkedRelatedField(
        many=False,
        read_only=True,
        view_name='fsobject-detail',
#        slug_field='pk',
        lookup_field='pk',
    )
#    parent = serializers.HyperlinkedModelSerializer()
    class Meta:
        model = FSObject
#        fields = '__all__'
        fields = '__all__'
        read_only_fields = ('name', 'parent','root')
#            'url', 'id', 'name', 'parent',
#        read_only_fields = fields
#        extra_kwargs = {
#            'url': {'view_name': 'buckets:fsobject', 'lookup_field': 'pk'}
#        }
