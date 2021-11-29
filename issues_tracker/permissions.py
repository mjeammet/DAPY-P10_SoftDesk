from rest_framework.permissions import BasePermission
from rest_framework.exceptions import APIException
from issues_tracker.models import Contributor, Permissions


class IsProjectContributor(BasePermission):

    def has_permission(self, request, view):
        user = request.user

        if user.is_superuser:
            return True

        user_contributions = [contrib.project_id for contrib in user.contributions.all()]
        project_id = get_project_id(view.kwargs)

        if project_id is None or int(project_id) in user_contributions:
            return True

    def has_object_permission(self, request, view, obj):
        user = request.user
        project_id = get_project_id(view.kwargs)
        user_contributions = [contrib.project_id for contrib in user.contributions.all()]

        if int(project_id) in user_contributions:
            return True


class IsObjectOwner(BasePermission):

    def has_object_permission(self, request, view, obj):
        if view.action in ['list', 'create', 'retrieve'] or obj.author_user == request.user:
            return True


class IsAuthorContributor(BasePermission):

    def has_object_permission(self, request, view, obj):
        project_id = get_project_id(view.kwargs)

        user_contrib = Contributor.objects.get(project_id=project_id, user=request.user)

        if user_contrib.permission == Permissions.AUTHOR:
            return True


def get_project_id(kwargs):
    project_id = kwargs['project_pk'] if 'project_pk' in kwargs else kwargs['pk'] if 'pk' in kwargs else None
    if project_id is None:
        return project_id
    else:
        try:
            return int(project_id)
        except ValueError:
            raise APIException({"details": 'Project ids must be integers.'})
