from django.contrib import admin
from django.urls import path, include
# from rest_framework import routers
from rest_framework_nested import routers

from issues_tracker.views import ProjectViewset, IssueViewset, CommentViewset, SignUpView

router = routers.DefaultRouter()
router.register('projects', ProjectViewset, basename='projects')

issues_router = routers.NestedSimpleRouter(router, 'projects', lookup='project')
issues_router.register('issues', IssueViewset, basename='issues')

comments_router = routers.NestedSimpleRouter(issues_router, 'issues', lookup='issue')
comments_router.register('comments', CommentViewset, basename='comments')

# router.register('issues', IssueViewset, basename='issues')
# router.register('comments', CommentViewset, basename='comments')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('signup/', SignUpView.as_view(), 'signup'),
    # path('login'),
    path('', include(router.urls)),
    path('', include(issues_router.urls)),
    path('', include(comments_router.urls)),
]
