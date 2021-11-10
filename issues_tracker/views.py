from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from issues_tracker.models import Project, Issue, Comment
from issues_tracker.serializers import ProjectListSerializer, IssueListSerializer, CommentListSerializer

class ProjectViewset(ReadOnlyModelViewSet):

    serializer_class = ProjectListSerializer

    def get_queryset(self):
        return Project.objects.all()


class IssueViewset(ReadOnlyModelViewSet):

    serializer_class = IssueListSerializer

    def get_queryset(self):
        return Issue.objects.filter(status="ONGOING")


class CommentViewset(ReadOnlyModelViewSet):

    serializer_class = CommentListSerializer

    def get_queryset(self):
        return Comment.objects.all()