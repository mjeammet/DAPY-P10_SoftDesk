from django.shortcuts import get_object_or_404
from rest_framework.permissions import BasePermission
from issues_tracker.models import Project

class IsProjectOwner(BasePermission):
    pass

    # def has_permission(self, request, view):
    #     project = get_object_or_404(Project, pk=view.kwargs['project_pk'])
    #     if request.user == project.author_user_id:
    #         return True
    #     else:
    #         return False
