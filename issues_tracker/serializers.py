from rest_framework.serializers import ModelSerializer

from issues_tracker.models import Project

class ProjectListSerializer(ModelSerializer):

    class Meta:
        model = Project
        fields = ['project_id', 'title', 'type']