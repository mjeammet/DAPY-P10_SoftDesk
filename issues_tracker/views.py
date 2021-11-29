from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.exceptions import APIException, ValidationError

from issues_tracker.models import Permissions, User, Project, Issue, Comment, Contributor
from issues_tracker.serializers import (
    UserSerializer,
    ProjectDetailSerializer, ProjectListSerializer,
    ContributorSerializer,
    IssueListSerializer, IssueDetailSerializer,
    CommentSerializer)
from issues_tracker.permissions import IsProjectContributor, IsAuthorContributor, IsObjectOwner


class SignUpView(ModelViewSet):

    serializer_class = UserSerializer
    permission_classes = [AllowAny]


class MultipleSerializerMixin:
    """Mixin to distinguish list from detail serializer."""

    detail_serializer_class = None

    def get_serializer_class(self):
        allowed_actions = ['retrieve', 'update', 'partial_update', 'create']
        if self.action in allowed_actions and self.detail_serializer_class is not None:
            # Si l'action demandée est le détail alors nous retournons le serializer de détail
            return self.detail_serializer_class
        return super().get_serializer_class()


class ProjectViewset(MultipleSerializerMixin, ModelViewSet):

    serializer_class = ProjectListSerializer
    detail_serializer_class = ProjectDetailSerializer
    permission_classes = (IsAuthenticated, IsProjectContributor, IsObjectOwner)

    def get_queryset(self):
        user = self.request.user
        users_projects = [contribution.project_id for contribution in Contributor.objects.filter(user=user)]
        queryset = Project.objects.filter(project_id__in=users_projects)
        return queryset

    def perform_create(self, serializer):
        """POST method to create a new project."""
        user = self.request.user
        project = serializer.save(author_user=user)
        Contributor.objects.create(user=user, project=project, permission=Permissions.AUTHOR)


class ContributorsViewset(ModelViewSet):

    serializer_class = ContributorSerializer
    permission_classes = (IsAuthenticated, IsProjectContributor, IsAuthorContributor)

    def get_queryset(self):
        project = get_object_or_404(Project, pk=self.kwargs['project_pk'])
        return project.users.all().order_by('permission')

    def perform_create(self, serializer):
        email = self.request.data.get('email')
        project_id = self.kwargs['project_pk']
        try:
            added_user = User.objects.get(email=email)
            project_id = Project.objects.get(pk=project_id)
        except User.DoesNotExist:
            raise APIException(f"No user with email \'{email}\'.")
        except Project.DoesNotExist:
            raise APIException(f"Project '{project_id}' does not exist.")

        if Contributor.objects.filter(user=added_user, project_id=project_id).exists():
            raise APIException("User already attached to project")
        else:
            serializer.save(user=added_user, project=project_id, permission=Permissions.CONTRIBUTOR)

    def destroy(self, request, pk=None, *args, **kwargs):
        try:
            contrib = Contributor.objects.get(pk=pk)
        except Contributor.DoesNotExist:
            raise APIException(f'No contribution with id {pk}')

        project_id = int(self.kwargs['project_pk'])
        if contrib.project_id == project_id and contrib.permission == Permissions.AUTHOR:
            raise APIException('Cannot remove project\'s author contributor from project')
        return super().destroy(self, request, pk=None, *args, **kwargs)
        # TODO What happens to your issues / comment when you are remove from a project ?


class IssueViewset(MultipleSerializerMixin, ModelViewSet):

    serializer_class = IssueListSerializer
    detail_serializer_class = IssueDetailSerializer
    permission_classes = (IsAuthenticated, IsProjectContributor, IsObjectOwner)

    def get_queryset(self):
        project = get_object_or_404(Project, pk=self.kwargs['project_pk'])
        if 'pk' in self.kwargs:
            issue = Issue.objects.filter(pk=self.kwargs['pk'], project=project)
            return issue
        else:
            return Issue.objects.filter(project=project)

    def perform_create(self, serializer):
        user = self.request.user
        project = get_object_or_404(Project, pk=self.kwargs['project_pk'])
        serializer.save(author_user=user, project=project, assignee_user=user)

    def perform_update(self, serializer):
        if serializer.is_valid():
            project_id = self.kwargs['project_pk']
            issue_pk = self.kwargs['pk']

            contributors = [contributor.user for contributor in Contributor.objects.filter(project_id=project_id)]
            if serializer.validated_data['assignee_user'] not in contributors:
                raise ValidationError({"detail": "Assignee must be a contributor for this project."})

            issue = Issue.objects.get(pk=issue_pk)
            serializer.save(instance=issue)


class CommentViewset(ModelViewSet):

    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticated, IsProjectContributor, IsObjectOwner)

    def get_queryset(self):
        issue = get_object_or_404(Issue, pk=self.kwargs['issue_pk'], project_id=self.kwargs['project_pk'])
        if 'pk' in self.kwargs:
            return Comment.objects.filter(pk=self.kwargs['pk'], issue=issue)
        else:
            return Comment.objects.filter(issue=issue)

    def perform_create(self, serializer):
        user = self.request.user
        issue = get_object_or_404(Issue, pk=self.kwargs['issue_pk'])
        serializer.save(author_user=user, issue=issue)
