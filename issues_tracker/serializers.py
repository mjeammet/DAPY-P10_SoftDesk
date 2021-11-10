from rest_framework.serializers import ModelSerializer

from issues_tracker.models import Project, Issue, Comment

class ProjectListSerializer(ModelSerializer):

    class Meta:
        model = Project
        fields = ['project_id', 'title', 'type']


class IssueListSerializer(ModelSerializer):

    class Meta:
        model = Issue
        fields = ['title', 'created_time', 'assignee_user_id']


class CommentListSerializer(ModelSerializer):

    class Meta:
        model = Comment
        fields = ['comment_id', 'created_time', 'author_user_id']