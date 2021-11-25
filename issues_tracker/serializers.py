from django.db.models.base import Model
from django.contrib.auth.hashers import make_password
from rest_framework.serializers import Serializer, ModelSerializer, SerializerMethodField, CharField, ValidationError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

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


class MyTokenObtainSerializer(ModelSerializer):
    username_field = User.EMAIL_FIELD

    # def __init__(self, *args, **kwargs):
    #     super(MyTokenObtainSerializer, self).__init__(*args, **kwargs)

    #     self.fields[self.username_field] = CharField()
    #     self.fields['password'] = PasswordField()

    def validate(self, attrs):
        # self.user = authenticate(**{
        #     self.username_field: attrs[self.username_field],
        #     'password': attrs['password'],
        # })
        print('\nUSERNAME_FIELD:', self.username_field)
        self.user = User.objects.get(email=attrs[self.username_field]).first()
        print(self.user)

        if not self.user:
            raise ValidationError('The user is not valid.')

        if self.user:
            if not self.user.check_password(attrs['password']):
                raise ValidationError('Incorrect credentials.')
        print(self.user)
        # Prior to Django 1.10, inactive users could be authenticated with the
        # default `ModelBackend`.  As of Django 1.10, the `ModelBackend`
        # prevents inactive users from authenticating.  App designers can still
        # allow inactive users to authenticate by opting for the new
        # `AllowAllUsersModelBackend`.  However, we explicitly prevent inactive
        # users from authenticating to enforce a reasonable policy and provide
        # sensible backwards compatibility with older Django versions.
        if self.user is None or not self.user.is_active:
            raise ValidationError('No active account found with the given credentials')

        return {}

    @classmethod
    def get_token(cls, user):
        raise NotImplemented(
            'Must implement `get_token` method for `MyTokenObtainSerializer` subclasses')

    class Meta:
        model = User
        fields = ['email', 'password']


class MyTokenObtainPairSerializer(MyTokenObtainSerializer):
    @classmethod
    def get_token(cls, user):
        return RefreshToken.for_user(user)

    def validate(self, attrs):
        data = super(MyTokenObtainPairSerializer, self).validate(attrs)

        refresh = self.get_token(self.user)

        data['refresh'] = text_type(refresh)
        data['access'] = text_type(refresh.access_token)

        return data


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
