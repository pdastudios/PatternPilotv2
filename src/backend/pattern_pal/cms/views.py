from rest_framework import viewsets, status, generics
from rest_framework.response import Response
from rest_framework.views import APIView

from django.http import Http404
from django.shortcuts import get_object_or_404

from .models import Project, Shape, Round
from .serializers import ProjectSerializer, ShapeSerializer, RoundSerializer



class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

# SHAPE REST FUNCTIONS
class ShapeViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for creating, retrieving, updating, and deleting rounds.
    """

    def list(self, request):
        queryset = Shape.objects.all()
        serializer = ShapeSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = ShapeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        queryset = Shape.objects.all()
        round_instance = get_object_or_404(queryset, pk=pk)
        serializer = ShapeSerializer(round_instance)
        return Response(serializer.data)

    def update(self, request, pk=None):
        round_instance = Shape.objects.get(pk=pk)
        serializer = ShapeSerializer(round_instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        round_instance = Shape.objects.get(pk=pk)
        round_instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# ROUND REST FUNCTIONS
class RoundViewSet(viewsets.ViewSet):
    """
    A simple ViewSet for creating, retrieving, updating, and deleting rounds.
    """

    def list(self, request):
        queryset = Round.objects.all()
        serializer = RoundSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = RoundSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        queryset = Round.objects.all()
        round_instance = get_object_or_404(queryset, pk=pk)
        serializer = RoundSerializer(round_instance)
        return Response(serializer.data)

    def update(self, request, pk=None):
        round_instance = Round.objects.get(pk=pk)
        serializer = RoundSerializer(round_instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        round_instance = Round.objects.get(pk=pk)
        round_instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class PatternView(APIView):
    def get(self, request, format=None):
        pattern = "pattern1"
        print("THIS WORKEDDDDDDDD")
        return Response({"pattern": pattern})