from django.db.models.base import Model
from rest_framework.serializers import ModelSerializer, SerializerMethodField

from issues_tracker.models import Project, Issue, Comment, Contributor, User


class UserSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ['username', 'password']


class ContributorSerializer(ModelSerializer):

    # user_id = serializers.ForeignKey()

    class Meta: 
        model = Contributor
        # fields = ['user_id', 'project_id', 'permission', 'role']
        fields = '__all__'

class ProjectListSerializer(ModelSerializer):

    class Meta:
        model = Project
        fields = ['project_id', 'title', 'type']


class ProjectDetailSerializer(ModelSerializer):

    class Meta:
        model = Project
        # fields = ['__all__']
        fields = ['project_id', 'title', 'description', 'type', 'author_user', 'active_issues_count']
        # Can't put '__all__' because it doesn't include the 'active_issues_count' property
        read_only = ['project_id', 'active_issues_count']


class IssueListSerializer(ModelSerializer):

    class Meta:
        model = Issue
        fields = ['id', 'title', 'assignee_user_id', 'created_time']


class IssueDetailSerializer(ModelSerializer):

    # comments = SerializerMethodField()

    class Meta:
        model = Issue
        fields = '__all__'

    # def get_comments(self, instance):
    #     queryset = instance.comments.all()
    #     serializer = CommentListSerializer(queryset, many=True)
    #     return serializer.data


class CommentListSerializer(ModelSerializer):

    class Meta:
        model = Comment
        fields = ['comment_id', 'author_user_id', 'created_time', 'issue_id']


class CommentDetailSerializer(ModelSerializer):

    class Meta: 
        model = Comment
        fields = ['comment_id', 'author_user_id', 'created_time', 'issue_id']