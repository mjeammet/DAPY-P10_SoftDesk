from django.contrib import admin
from django.urls import path, include
# from rest_framework import routers
from rest_framework_nested import routers

from issues_tracker.views import ProjectViewset, IssueViewset, CommentViewset

router = routers.SimpleRouter()
router.register('projects', ProjectViewset, basename='projects')

issues_router = routers.NestedSimpleRouter(router, 'projects', lookup='project')
issues_router.register('issues', IssueViewset, basename='project-issues')

# router.register('issues', IssueViewset, basename='issues')
router.register('comments', CommentViewset, basename='comments')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    # path('signup/', SignUpViewset.as_view(), 'signup'),
    # path('login'),
    path('', include(router.urls)),
    path('', include(issues_router.urls)),
]
