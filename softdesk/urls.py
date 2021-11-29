from django.contrib import admin
from django.urls import path, include
# from rest_framework import routers
from rest_framework_nested import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

# from issues_tracker.serializers import MyTokenObtainPairSerializer
from issues_tracker.views import ProjectViewset, IssueViewset, CommentViewset, SignUpView, ContributorsViewset

router = routers.SimpleRouter()
router.register('projects', ProjectViewset, basename='projects')
users_router = routers.NestedSimpleRouter(router, 'projects', lookup='project')
users_router.register('users', ContributorsViewset, basename='users')
# TODO remove unwanted retrieve / patch / put route
# [print(route) for route in router.urls if route in ['GET', 'create', 'destroy']]
# users_router._urls = [route for route in router.urls if route in ['GET', 'create', 'destroy']]
issues_router = routers.NestedSimpleRouter(router, 'projects', lookup='project')
issues_router.register('issues', IssueViewset, basename='issues')
comments_router = routers.NestedSimpleRouter(issues_router, 'issues', lookup='issue')
comments_router.register('comments', CommentViewset, basename='comments')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('signup/', SignUpView.as_view({'post': 'create'}), name='signup'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', include(router.urls)),
    path('', include(users_router.urls)),
    path('', include(issues_router.urls)),
    path('', include(comments_router.urls)),
]
