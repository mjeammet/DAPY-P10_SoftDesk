from rest_framework.serializers import ModelSerializer, SerializerMethodField

from issues_tracker.models import Project, Issue, Comment, Contributor, User


class UserSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ['username', 'password']


class ContributorSerializer(ModelSerializer):

    class Meta: 
        model = Contributor
        fields = ['user_id', 'project_id', 'permission', 'role']


class ProjectListSerializer(ModelSerializer):

    class Meta:
        model = Project
        fields = ['project_id', 'title', 'type']


class ProjectDetailSerializer(ModelSerializer):

    class Meta:
        model = Project
        fields = ['title', 'description', 'type', 'active_issues_count', 'author_user']
        read_only = ['project_id']
        # fields = '__all__'


class IssueListSerializer(ModelSerializer):

    class Meta:
        model = Issue
        fields = ['title', 'assignee_user_id', 'created_time']


class IssueDetailSerializer(ModelSerializer):

    # comments = SerializerMethodField()

    class Meta:
        model = Issue
        fields = ['title', 'desc', 'tag', 'status', 'author_user_id', 'assignee_user_id', 'created_time', 'comments']

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