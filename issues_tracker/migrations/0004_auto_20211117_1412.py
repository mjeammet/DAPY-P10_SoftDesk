# Generated by Django 3.2.9 on 2021-11-17 14:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('issues_tracker', '0003_auto_20211115_1648'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='author_user_id',
            new_name='author_user',
        ),
        migrations.RenameField(
            model_name='comment',
            old_name='issue_id',
            new_name='issue',
        ),
        migrations.RenameField(
            model_name='contributor',
            old_name='project_id',
            new_name='project',
        ),
        migrations.RenameField(
            model_name='contributor',
            old_name='user_id',
            new_name='user',
        ),
        migrations.RenameField(
            model_name='issue',
            old_name='assignee_user_id',
            new_name='assignee_user',
        ),
        migrations.RenameField(
            model_name='issue',
            old_name='author_user_id',
            new_name='author_user',
        ),
        migrations.RenameField(
            model_name='issue',
            old_name='project_id',
            new_name='project',
        ),
        migrations.RenameField(
            model_name='project',
            old_name='author_user_id',
            new_name='author_user',
        ),
    ]