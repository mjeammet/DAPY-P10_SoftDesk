from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet, ViewSet

from issues_tracker.models import Project, Issue, Comment
from issues_tracker.serializers import IssueDetailSerializer, ProjectDetailSerializer, ProjectListSerializer, IssueListSerializer, CommentListSerializer

# AUTHENTICATION RELATED CLASSES
class SignUpViewset(ViewSet):
    pass 


class ProjectViewset(ReadOnlyModelViewSet):

    serializer_class = ProjectListSerializer
    detail_serializer_class = ProjectDetailSerializer

    def get_queryset(self):
        return Project.objects.all()

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return self.detail_serializer_class
        else:
            return super().get_serializer_class()


class IssueViewset(ReadOnlyModelViewSet):

    serializer_class = IssueListSerializer
    detail_serializer_class = IssueDetailSerializer

    def get_queryset(self):
        return Issue.objects.all()

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return self.detail_serializer_class
        else:
            return super().get_serializer_class()


class CommentViewset(ReadOnlyModelViewSet):

    serializer_class = CommentListSerializer

    def get_queryset(self):
        return Comment.objects.all()