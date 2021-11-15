from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from issues_tracker.models import Project, Issue, Comment
<<<<<<< HEAD
from issues_tracker.serializers import ProjectListSerializer, IssueListSerializer, CommentListSerializer
=======
from issues_tracker.serializers import IssueDetailSerializer, ProjectDetailSerializer, ProjectListSerializer, IssueListSerializer, CommentListSerializer

>>>>>>> 830e6de2fc14022f3fa3dfa5e1e3fdd49d949899

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
<<<<<<< HEAD
        return Project.objects.all()


class IssueViewset(ReadOnlyModelViewSet):

    serializer_class = IssueListSerializer

    def get_queryset(self):
        return Issue.objects.filter(status="ONGOING")


class CommentViewset(ReadOnlyModelViewSet):

    serializer_class = CommentListSerializer

    def get_queryset(self):
=======
>>>>>>> 830e6de2fc14022f3fa3dfa5e1e3fdd49d949899
        return Comment.objects.all()