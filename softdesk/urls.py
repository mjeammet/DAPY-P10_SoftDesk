from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from issues_tracker.views import ProjectViewset

router = routers.SimpleRouter()
router.register('projects', ProjectViewset, basename='projects')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls))
]
