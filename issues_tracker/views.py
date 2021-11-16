from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, GenericAPIView
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet, ViewSet
from rest_framework import serializers

from issues_tracker.models import User, Project, Issue, Comment, Contributor
from issues_tracker.serializers import (
    UserSerializer, ContributorSerializer, 
    ProjectDetailSerializer, ProjectListSerializer, 
    IssueListSerializer, IssueDetailSerializer, 
    CommentListSerializer, CommentDetailSerializer)


#-----------------------------------#
#   AUTHENTICATION RELATED CLASSES  #
#-----------------------------------#

# class SignUpView(ModelViewSet):

#     serializer_class = UserSerializer

#     def get_queryset(self):
#         return User.objects.all()

#     def validate_username(self, value):
#         if User.objects.filter(username=value).exists():
#             raise serializers.ValidationError("Username already exists.")
#         return value


class SignUpView(APIView):
    
    serializer_class = UserSerializer

    def get(self):
        return User.objects.all()

    def post(self, request):
        user = request.data
        serializer = UserSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        # return Response(serializer.data, status=status.HTTP_201_CREATED)


class LogInView(GenericAPIView):

    serializer_class = UserSerializer

    def post(self):
        return    


class ContributorsViewset(ModelViewSet):

    serializer_class = ContributorSerializer
    # detail_serializer_class = UserDetailSerializer

    def get_queryset(self):
        return Contributor.objects.all()


#-----------------------------------#
#       PROJECTS RELATED VIEWS      #
#-----------------------------------#


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
        project_id = get_object_or_404(Project, pk=self.kwargs['project_pk'])
        return Issue.objects.filter(project_id=project_id)

    def get_serializer_class(self):
        if self.action == 'retrieve':   
            return self.detail_serializer_class
        else:
            return super().get_serializer_class()


class CommentViewset(ReadOnlyModelViewSet):

    serializer_class = CommentListSerializer
    detail_serializer_class = CommentDetailSerializer

    def get_queryset(self):
        return Comment.objects.all()

    def get_serializer_class(self):
        if self.action == 'retrieve':   
            return self.detail_serializer_class
        else:
            return super().get_serializer_class()
