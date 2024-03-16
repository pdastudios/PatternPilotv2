from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, Serializer
from django.contrib.auth.models import User
from .models import Project, Shape, Round

class ProjectSerializer(ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'name','author','created','modified']

class ShapeSerializer(ModelSerializer):
    class Meta:
        model = Shape
        fields = ['id', 'name','project','total_rounds','total_stitches']


class RoundSerializer(ModelSerializer):
    class Meta:
        model = Round
        fields = ['id','formula','result','shape','comment']


