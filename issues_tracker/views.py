from django.shortcuts import render
from rest_framework.generics import CreateAPIView
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet, ViewSet
from rest_framework import serializers

from issues_tracker.models import User, Project, Issue, Comment
from issues_tracker.serializers import IssueDetailSerializer, ProjectDetailSerializer, ProjectListSerializer, IssueListSerializer, CommentListSerializer

# AUTHENTICATION RELATED CLASSES
# class SignUpView(ModelViewSet):
class SignUpView(CreateAPIView):

    def get_queryset(self):
        return 

    # def validate_username(self, value):
    #     if User.objects.filter(username=value).exists():
    #         raise serializers.ValidationError("Username already exists.")
    #     return value


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
        return Issue.objects.filter(project_id=self.kwargs['project_pk'])

    def get_serializer_class(self):
        if self.action == 'retrieve':   
            return self.detail_serializer_class
        else:
            return super().get_serializer_class()


class CommentViewset(ReadOnlyModelViewSet):

    serializer_class = CommentListSerializer

    def get_queryset(self):
        return Comment.objects.all()
