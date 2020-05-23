from rest_framework import serializers
from .models import Polygon


class PolygonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Polygon
        fields = '__all__'


class PartialPolygonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Polygon
        fields = ['id', 'name']
