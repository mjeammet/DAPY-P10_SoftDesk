from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from issues_tracker.views import ProjectViewset, IssueViewset, CommentViewset

router = routers.SimpleRouter()
router.register('projects', ProjectViewset, basename='projects')
router.register('issues', IssueViewset, basename='issues')
router.register('comments', CommentViewset, basename='comments')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls))
]
