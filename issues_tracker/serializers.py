from django.contrib.auth.hashers import make_password
from rest_framework.serializers import ModelSerializer, ValidationError
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
        fields = ['project_id', 'user_id', 'permission', 'role', 'id']


class ProjectListSerializer(ModelSerializer):

    class Meta:
        model = Project
        fields = ['project_id', 'title', 'author_user', 'type']

    def validate_title(self, value):
        if len(value) < 5:
            raise ValidationError("Titles must be at least 5 caracters long")
        return value


class ProjectDetailSerializer(ModelSerializer):

    class Meta:
        model = Project
        fields = ['project_id', 'title', 'author_user_id', 'description', 'type', 'active_issues_count']
        # Can't put '__all__' because it doesn't include the 'active_issues_count' property
        read_only = ['project_id', 'author_user_id', 'active_issues_count']


class IssueListSerializer(ModelSerializer):

    class Meta:
        model = Issue
        fields = ['id', 'title', 'priority', 'author_user_id', 'assignee_user_id']


class IssueDetailSerializer(ModelSerializer):

    class Meta:
        model = Issue
        fields = ['id', 'title', 'priority', 'project_id', 'desc', 'tag', 'status', 'author_user_id', 'assignee_user']
        read_only = ['project_id', 'author_user_id']

    # TODO Add a validate that makes sure assignee_user is in Contributor.objects.filter(project_id=project_id)
    # Issue being that I don't know how to get project_id :/
    # def validate_assignee_user(self, value):
    #     if value not in Contributor.objects.filter(project_id=self.kwargs['project_pk']):
    #         return value
    #     else:
    #         return ValidationError('Cannot assign issue to non-contributors.')
    # def validate(self, data):
    #     contributors = [contrib.user_id for contrib in Contributor.objects.filter(project_id=project_id)]
    #     if data['assignee_user'] not in contributors:
    #         raise ValidationError("Assignee must be a contributor of this project.")


class CommentSerializer(ModelSerializer):

    class Meta:
        model = Comment
        fields = ['project_id', 'issue_id', 'comment_id', 'description', 'author_user_id', 'created_time']
        read_only = ['project_id', 'author_user', 'issue']
