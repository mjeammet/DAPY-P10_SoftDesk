from django.shortcuts import get_object_or_404
from rest_framework.permissions import BasePermission, SAFE_METHODS
from issues_tracker.models import Project, Contributor, Permissions


class IsProjectAuthorized(BasePermission):

    def has_permission(self, request, view):
        user = request.user

        if user.is_superuser:
            return True

        user_contributions = [contrib.project_id for contrib in user.contributions.all()]
        # print('KWARGS =', view.kwargs, ' and authorized projects ids = ', user_contributions)
        try:
            project_id = int(view.kwargs['project_pk']) if 'project_pk' in int(view.kwargs) else view.kwargs['pk'] if 'pk' in view.kwargs else None
            if project_id in user_contributions:
                return True
            else:
                return False
        except:
            return True

    def has_object_permission(self, request, view, obj):
        project_id = int(view.kwargs['project_pk']) if 'project_pk' in view.kwargs else int(view.kwargs['pk']) if 'pk' in view.kwargs else None

        if request.user.is_superuser or request.method in SAFE_METHODS:
            return True

        # print("User: ", request.user, " and project's owner: ", obj.author_user)
        # print("action: ", request.method)
        # print('View: ', view.action)
        if isinstance(obj, Contributor):
            if view.action in ["retrieve" , "update"]:
                return False

            # # Not having any direction regarding contributors, I'll allow only the author to 
            if Contributor.objects.get(project_id=project_id, user=request.user).permission == Permissions.AUTHOR:
                return True
            else:
                return False
        else:
            if request.user == obj.author_user:
                return True
            else:
                return False


class CanModifyContributors(BasePermission):

    def has_object_permission(self, request, view, obj):
        pass