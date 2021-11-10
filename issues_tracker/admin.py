from django.contrib import admin

# Register your models here.
from .models import User, Project, Issue, Comment

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'type']
    exclude = ['project_id']


@admin.register(Issue)
class IssueAdmin(admin.ModelAdmin):
    pass


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    pass