from rest_framework.serializers import ModelSerializer
from django.contrib.auth.models import User
from .models import Project

class ProjectSerializer(ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'name','author','created','modified']