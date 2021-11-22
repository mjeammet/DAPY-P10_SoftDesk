from django.shortcuts import render, get_object_or_404
from django.template.defaultfilters import add
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, GenericAPIView
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet, ViewSet
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.decorators import api_view
from rest_framework.exceptions import APIException

from issues_tracker.models import Permissions, User, Project, Issue, Comment, Contributor
from issues_tracker.serializers import (
    UserSerializer, ContributorSerializer, 
    ProjectDetailSerializer, ProjectListSerializer, 
    IssueListSerializer, IssueDetailSerializer, 
    CommentListSerializer, CommentDetailSerializer)
from issues_tracker.permissions import IsProjectOwner


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

    def get_queryset(self):
        users_projects = [contribution.project_id for contribution in Contributor.objects.filter(user=self.request.user)]
        queryset = Project.objects.filter(project_id__in=users_projects)
        # TODO handle permissions (should not access/edit if not contributor, should not delete if not author)
        return queryset

    # def get_permissions(self):
    #     permission_classes = [IsAuthenticated]

    #     if self.action == 'destroy':
    #         permission_classes.append(IsProjectOwner)

    def perform_create(self, serializer):
        """POST method to create a new project."""
        user = self.request.user
        project = serializer.save(author_user=user)
        Contributor.objects.create(
            user = user,
            project = project,
            permission = Permissions.AUTHOR
        )

    # TODO check if I can use decorators to specify which method and/or give specific permission_classes to method
    # @api_view(['POST'])
    # @permission_classes([IsProjectOwner])
    # def destroy(self, request, pk=None):
    #     super().destroy(request, pk=None)


class ContributorsViewset(ModelViewSet):

    serializer_class = ContributorSerializer
    # detail_serializer_class = UserSerializer

    def get_queryset(self):
        project = get_object_or_404(Project, pk=self.kwargs['project_pk'])
        # return Contributor.objects.filter(project=project)
        return project.users.all()

    def perform_create(self, serializer):
        submitted_username = self.request.data.get('username')
        added_user = User.objects.get(username=submitted_username)
        project_id = Project.objects.get(pk=self.kwargs['project_pk'])
        # if project_id:
        if Contributor.objects.filter(user=added_user, project_id=project_id).exists():
            raise APIException("User already attached to project")
        else:
            try:
                serializer.save(user=added_user, project=project_id, permission=Permissions.CONTRIBUTOR)
            # for some reasons, does not exist are not caught
            # TODO Handle unknown project / unknown user addition
            except Project.DoesNotExist:
                raise APIException(f"Project '{project_id}' does not exist.")
            except User.DoesNotExist:
                raise APIException("User doesn't exist")

    # TODO Ask if id should be id of user to remove or id of contribution

    # @api_view(['DELETE'])
    # def remove_contributor(self, pk=None):
    #     print("\n\nDELETE TEST\n")

    # @api_view(['DELETE'])
    # @permission_classes(...)
    # def destroy(self, request, pk=None):
    #     print("\n\nANOTHER TEST\n")
    #     return Response()


class IssueViewset(MultipleSerializerMixin, ModelViewSet):

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
