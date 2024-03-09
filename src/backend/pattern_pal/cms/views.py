from django.shortcuts import render
from django.contrib.auth.models import User

from django.conf import settings

from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ViewSet
from rest_framework.decorators import api_view, action

from .models import Project
from .serializers import ProjectSerializer

class ProjectViewSet(ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer