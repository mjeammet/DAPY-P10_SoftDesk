from django.contrib import admin
from django.urls import path, include
# from rest_framework import routers
from rest_framework_nested import routers

from issues_tracker.views import ProjectViewset, IssueViewset, CommentViewset, SignUpView, LogInView, ContributorsViewset

router = routers.SimpleRouter()
router.register('projects', ProjectViewset, basename='projects')
users_router = routers.NestedSimpleRouter(router, 'projects', lookup='project')
users_router.register('users', ContributorsViewset, basename='users')
issues_router = routers.NestedSimpleRouter(router, 'projects', lookup='project')
issues_router.register('issues', IssueViewset, basename='issues')
comments_router = routers.NestedSimpleRouter(issues_router, 'issues', lookup='issue')
comments_router.register('comments', CommentViewset, basename='comments')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    # path('signup/', SignUpView.as_view({'get':'list'}), 'signup'),
    path('signup/', SignUpView, 'signup'),
    path('login/', LogInView.as_view(), 'login'),
    path('', include(router.urls)),
    path('', include(users_router.urls)),
    path('', include(issues_router.urls)),
    path('', include(comments_router.urls)),
]
