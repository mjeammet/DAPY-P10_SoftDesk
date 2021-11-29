from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings


class Types(models.TextChoices):
    BACK = "Back-end"
    FRONT = "Front-end"
    IOS = "iOS"
    ANDR = "Android"
    __empty__ = "Unspecified"


class Status(models.TextChoices):
    TODO = "Todo"
    ONGOING = "En cours"
    DONE = "Terminé"


class Permissions(models.TextChoices):
    AUTHOR = 'Author'
    CONTRIBUTOR = 'Contributor'


class Priority(models.TextChoices):
    LOW = 'Basse'
    AVERAGE = 'Moyenne'
    HIGH = "Haute"


class User(AbstractUser):
    email = models.EmailField(verbose_name='email address', max_length=255, unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


class Project(models.Model):
    project_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=150)
    description = models.CharField(max_length=2048)
    type = models.CharField(max_length=10, choices=Types.choices, default=Types.__empty__)
    author_user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='projects')

    def __str__(self):
        return f'{self.title} (P{self.project_id})'

    @property
    def active_issues_count(self):
        return self.issues.exclude(status=Status.DONE).count()


class Contributor(models.Model):
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='contributions')
    project = models.ForeignKey(to=Project, on_delete=models.CASCADE, related_name="users")
    permission = models.CharField(
        choices=Permissions.choices,
        max_length=11,
        blank=False,
        null=False,
        default=Permissions.CONTRIBUTOR)
    role = models.CharField(max_length=128, blank=True, null=True)

    def __str__(self):
        return f'{self.user} is {self.permission.lower()} on P{self.project_id}'


class Issue(models.Model):
    # issue_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=150)
    desc = models.CharField(max_length=2048)
    tag = models.CharField(max_length=150, blank=True, null=True)
    priority = models.CharField(max_length=10, choices=Priority.choices, default=Priority.AVERAGE)
    project = models.ForeignKey(to=Project, related_name='issues', on_delete=models.CASCADE, blank=False, null=False)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.TODO)
    author_user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='issues')
    assignee_user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='tasks', blank=True, null=True)
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.title} (#{self.id})'

    class Meta:
        ordering = ['created_time']


class Comment(models.Model):
    comment_id = models.AutoField(primary_key=True)
    description = models.CharField(max_length=2048)
    author_user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comments')
    issue = models.ForeignKey(to=Issue, on_delete=models.CASCADE, related_name='comments')
    created_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_time']

    def __str__(self):
        return f'Comment {self.comment_id}, by {self.author_user}'

    @property
    def project_id(self):
        return int(self.issue.project.id)
