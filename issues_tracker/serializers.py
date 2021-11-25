from django.db.models.base import Model
from django.contrib.auth.hashers import make_password
from rest_framework.serializers import ModelSerializer, SerializerMethodField, CharField, ValidationError


from issues_tracker.models import Project, Issue, Comment, Contributor, User


class UserSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password']

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise ValidationError('email already registered.')
        return value

    def validate_password(self, value):
        """Hashes password."""
        if len(value) < 8:
            raise ValidationError('Password must be at least 8 characters')
        return make_password(value)

    def validate(self, data):
        first_name = data['first_name']
        last_name = data['last_name']
        email = data['email']

        if first_name.isalnum() and last_name.isalnum():
            # data['username'] = f'{last_name.lower()}_{first_name.lower()}'
            data['username'] = email
            return data
        else:
            raise ValidationError('First and last names must be only numeric.')


class ContributorSerializer(ModelSerializer):

    class Meta: 
        model = Contributor
        fields = ['user_id', 'project_id', 'permission', 'role']
        # fields = '__all__'


class ProjectListSerializer(ModelSerializer):

    class Meta:
        model = Project
        fields = ['project_id', 'title', 'author_user', 'type']


class ProjectDetailSerializer(ModelSerializer):

    class Meta:
        model = Project
        fields = ['project_id', 'title', 'author_user_id', 'description', 'type', 'active_issues_count']
        # Can't put '__all__' because it doesn't include the 'active_issues_count' property
        read_only = ['project_id', 'author_user_id', 'active_issues_count']


class IssueListSerializer(ModelSerializer):

    class Meta:
        model = Issue
        fields = ['id', 'title', 'author_user_id', 'created_time', 'assignee_user_id']


class IssueDetailSerializer(ModelSerializer):

    # comments = SerializerMethodField()

    class Meta:
        model = Issue
        # fields = '__all__'
        fields = ['id', 'title', 'project_id', 'desc', 'tag', 'status', 'author_user_id', 'assignee_user']
        read_only = ['project_id', 'author_user_id']

    # def get_comments(self, instance):
    #     queryset = instance.comments.all()
    #     serializer = CommentListSerializer(queryset, many=True)
    #     return serializer.data


class CommentSerializer(ModelSerializer):

    class Meta:
        model = Comment
        fields = ['project_id', 'issue_id', 'comment_id', 'description', 'author_user_id', 'created_time']
        # Can't "fields = '__all__'" because then read_only doesn't work anymore :/
        read_only = ['project_id', 'author_user', 'issue']
