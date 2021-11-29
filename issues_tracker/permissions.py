from django.shortcuts import get_object_or_404
from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework.exceptions import APIException
from issues_tracker.models import Issue, Project, Contributor, Permissions


class IsProjectContributor(BasePermission):

    def has_permission(self, request, view):
        user = request.user

        if user.is_superuser:
            return True

        user_contributions = [contrib.project_id for contrib in user.contributions.all()]
        # print('KWARGS =', view.kwargs, ' and authorized projects ids = ', user_contributions)

        project_id = int(view.kwargs['project_pk']) if 'project_pk' in view.kwargs else int(view.kwargs['pk']) if 'pk' in view.kwargs else None
        if project_id in user_contributions:
            return True

    def has_object_permission(self, request, view, obj):
        user = request.user
        project_id = view.kwargs['project_pk']
        user_contributions = [contrib.project_id for contrib in user.contributions.all()]

        if project_id in user_contributions and (view.action == 'retrieve' or request.user == obj.author_user):
            return True


class IsObjectOwner(BasePermission):

    def has_object_permission(self, request, view, obj):
        # if isinstance(obj, Issue) and obj.project != 

        if request.user.is_superuser:
            return True

        if request.user == obj.author_user:
            return True


class IsAuthorContributor(BasePermission):

    def has_object_permission(self, request, view, obj):
        project_id = int(view.kwargs['project_pk']) if 'project_pk' in view.kwargs else int(view.kwargs['pk']) if 'pk' in view.kwargs else None
        # Not having any direction regarding contributors, I'll allow only the author to 

        user_contrib = Contributor.objects.get(project_id=project_id, user=request.user)
        
        if user_contrib.permission == Permissions.AUTHOR:
            return True
