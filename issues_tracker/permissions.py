from django.shortcuts import get_object_or_404
from rest_framework.permissions import BasePermission, SAFE_METHODS
from issues_tracker.models import Project, Contributor
from rest_framework.exceptions import APIException

class IsProjectOwner(BasePermission):

    def has_permission(self, request, view):        
        project = get_object_or_404(Project, pk=view.kwargs['project_pk'])
        # TODO Use contribution table instead of project's foreign key to user 
        if request.user == project.author_user:
            return True
        else:
            return False


class IsProjectAuthorized(BasePermission):

    def has_permission(self, request, view):
        user_contributions = [contrib.project_id for contrib in Contributor.objects.filter(user=request.user)]
        print('KWARGS =', view.kwargs, ' and authorized projects ids = ', user_contributions)
        try:
            project_id = int(view.kwargs['project_pk']) if 'project_pk' in int(view.kwargs) else view.kwargs['pk'] if 'pk' in view.kwargs else None

            # TODO Remove permissions for update and deletion if not Owner

            if project_id in user_contributions:
                return True
            else:
                return False
        except:
            return True

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True

        print("User: ", request.user, " and project's owner: ", obj.author_user)
        print("action: ", request.method)
        print('View: ', view.action)
        if request.method in SAFE_METHODS:
            return True
        else:
            if request.user == obj.author_user:
                return True
            else:
                return False