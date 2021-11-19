from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, GenericAPIView
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet, ViewSet
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import serializers, status

from issues_tracker.models import Permissions, User, Project, Issue, Comment, Contributor
from issues_tracker.serializers import (
    UserSerializer, ContributorSerializer, 
    ProjectDetailSerializer, ProjectListSerializer, 
    IssueListSerializer, IssueDetailSerializer, 
    CommentListSerializer, CommentDetailSerializer)


#-----------------------------------#
#   AUTHENTICATION-RELATED CLASSES  #
#-----------------------------------#


class SignUpView(ModelViewSet):
    
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    # def get(self):
    #     return User.objects.all()

    def create(self, request):
        serializer = UserSerializer(data = request.data)        
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

#-----------------------------------#
#       PROJECTS-RELATED VIEWS      #
#-----------------------------------#

class MultipleSerializerMixin:
    """Mixin to distinguish list from detail serializer."""

    detail_serializer_class = None

    def get_serializer_class(self):
        if self.action in ['retrieve', 'update', 'partial_update', 'create'] and self.detail_serializer_class is not None:
            # Si l'action demandée est le détail alors nous retournons le serializer de détail
            return self.detail_serializer_class
        return super().get_serializer_class()


class ProjectViewset(MultipleSerializerMixin, ModelViewSet):

    serializer_class = ProjectListSerializer
    detail_serializer_class = ProjectDetailSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user_projects = [project.id for project in Contributor.objects.filter(user=self.request.user)]
        queryset = Project.objects.filter(project_id__in=user_projects)
        # TODO remove permission to edit projects where user is not a contributor
        # if self.request.GET.get('project_id'):
        #     project_id = self.request.GET.get('project_id')
        #     queryset = Project.objects.filter(project_id=project_id)
        #     self.check_object_permissions(self.request, queryset)
        return queryset

    def perform_create(self, serializer):
        """POST method to create a new project."""
        user = self.request.user
        project = serializer.save(author_user=user)
        Contributor.objects.create(
            user = user,
            project = project,
            permission = Permissions.AUTHOR
        )

    # def destroy(self, request, pk=None):
    #     print("\n\nBON !!_\n\n")


class ContributorsViewset(ModelViewSet):

    serializer_class = ContributorSerializer
    # detail_serializer_class = UserDetailSerializer

    def get_queryset(self):
        project_id = get_object_or_404(Project, pk=self.kwargs['project_pk'])
        return Contributor.objects.filter(project_id=project_id)


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
