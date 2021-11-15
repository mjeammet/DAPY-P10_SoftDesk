from rest_framework.serializers import ModelSerializer, SerializerMethodField

from issues_tracker.models import Project, Issue, Comment

class ProjectListSerializer(ModelSerializer):

    class Meta:
        model = Project
        fields = ['project_id', 'title', 'type']


<<<<<<< HEAD
=======
class ProjectDetailSerializer(ModelSerializer):

    # issues = SerializerMethodField() ?

    class Meta:
        model = Project
        fields = ['project_id', 'title', 'type', 'author_user_id', 'description']


>>>>>>> 830e6de2fc14022f3fa3dfa5e1e3fdd49d949899
class IssueListSerializer(ModelSerializer):

    class Meta:
        model = Issue
<<<<<<< HEAD

=======
        fields = ['title', 'assignee_user_id', 'created_time']


class IssueDetailSerializer(ModelSerializer):

    comments = SerializerMethodField()

    class Meta:
        model = Issue
        fields = ['title', 'desc', 'tag', 'status', 'author_user_id', 'assignee_user_id', 'created_time', 'comments']

    def get_comments(self, instance):
        queryset = instance.comments.all()
        serializer = CommentListSerializer(queryset, many=True)
        return serializer.data
>>>>>>> 830e6de2fc14022f3fa3dfa5e1e3fdd49d949899


class CommentListSerializer(ModelSerializer):

    class Meta:
        model = Comment
        fields = ['comment_id', 'author_user_id', 'created_time', 'issue_id']

