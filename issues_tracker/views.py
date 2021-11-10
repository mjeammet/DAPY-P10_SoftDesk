from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from issues_tracker.models import Project
from issues_tracker.serializers import ProjectListSerializer

class ProjectViewset(ReadOnlyModelViewSet):

    serializer_class = ProjectListSerializer

    def get_queryset(self):
        return Project.objects.all()