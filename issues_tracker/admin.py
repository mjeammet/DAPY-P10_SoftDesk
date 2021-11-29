from django.contrib import admin

# Register your models here.
from .models import Project, Issue, Comment, Contributor


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


@admin.register(Contributor)
class ContributorAdmin(admin.ModelAdmin):
    pass
