from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, GenericAPIView
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet, ViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework import serializers

from issues_tracker.models import PERMISSIONS, User, Project, Issue, Comment, Contributor
from issues_tracker.serializers import (
    UserSerializer, ContributorSerializer, 
    ProjectDetailSerializer, ProjectListSerializer, 
    IssueListSerializer, IssueDetailSerializer, 
    CommentListSerializer, CommentDetailSerializer)


#-----------------------------------#
#   AUTHENTICATION-RELATED CLASSES  #
#-----------------------------------#

# class SignUpView(ModelViewSet):

#     serializer_class = UserSerializer

#     def get_queryset(self):
#         return User.objects.all()

#     def validate_username(self, value):
#         if User.objects.filter(username=value).exists():
#             raise serializers.ValidationError("Username already exists.")
#         return value


class SignUpView(CreateAPIView):
    
    serializer_class = UserSerializer

    def get(self):
        return User.objects.all()

    # def post(self, request):
    #     user = request.data
    #     serializer = UserSerializer(data = request.data)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #     # return Response(serializer.data, status=status.HTTP_201_CREATED)


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
#       PROJECTS-RELATED VIEWS      #
#-----------------------------------#


class MultipleSerializerMixin:
    """Mixin to distinguish list from detail serializer."""

    detail_serializer_class = None

    def get_serializer_class(self):
        if self.action in ['retrieve', 'create'] and self.detail_serializer_class is not None:
            # Si l'action demandée est le détail alors nous retournons le serializer de détail
            return self.detail_serializer_class
        return super().get_serializer_class()

class ProjectViewset(MultipleSerializerMixin, ModelViewSet):

    serializer_class = ProjectListSerializer
    detail_serializer_class = ProjectDetailSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Project.objects.filter(project_id__in=[project.id for project in Contributor.objects.filter(user=user)])

    def perform_create(self, serializer):
        """ #TODO use CreateModelMixin (from rest_framework.mixins) instead."""
        user = self.request.user
        project = serializer.save(author_user=user)
        Contributor.objects.create(
            user = user,
            project = project,
            permission = PERMISSIONS[0]
        )


class IssueViewset(MultipleSerializerMixin, ReadOnlyModelViewSet):

    serializer_class = IssueListSerializer
    detail_serializer_class = IssueDetailSerializer

    def get_queryset(self):
        project_id = get_object_or_404(Project, pk=self.kwargs['project_pk'])
        return Issue.objects.filter(project_id=project_id)


class CommentViewset(MultipleSerializerMixin, ReadOnlyModelViewSet):

    serializer_class = CommentListSerializer
    detail_serializer_class = CommentDetailSerializer

    def get_queryset(self):
        return Comment.objects.all()
