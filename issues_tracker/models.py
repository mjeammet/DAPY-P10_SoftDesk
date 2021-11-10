from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

PRIORITY_LIST = ["Low", "Medium", "High"]


class User(AbstractUser):
    pass


class Types(models.TextChoices):
    BACK = "Back-end"
    FRONT = "Front-end"
    IOS = "iOS"
    ANDR = "Android"
    __empty__ = "Unspecified"


class Status(models.TextChoices):
    TODO = "A faire"
    ONGOING = "En cours"
    DONE = "Terminé"


class Project(models.Model):
    project_id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=150)
    description = models.CharField(max_length=2048)
    type = models.CharField(max_length=10, choices=Types.choices, default=Types.__empty__)
    author_user_id = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='projects')


class Issue(models.Model):
    title = models.CharField(max_length=150)
    desc = models.CharField(max_length=2048)
    tag = models.CharField(max_length=150)
    # priority = models.CharField(max_length=10)
    # project_id = models.ForeignKey()
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.TODO)
    author_user_id = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    assignee_user_id = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='issues')
    created_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_time']


class Comment(models.Model):
    comment_id = models.IntegerField(primary_key=True)
    description = models.CharField(max_length=2048)
    author_user_id = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comments')
    issue_id = models.ForeignKey(to=Issue, on_delete=models.CASCADE, related_name='comments')
    created_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_time']
