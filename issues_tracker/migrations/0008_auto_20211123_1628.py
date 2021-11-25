# Generated by Django 3.2.9 on 2021-11-23 16:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('issues_tracker', '0007_auto_20211123_0040'),
    ]

    operations = [
        migrations.AlterField(
            model_name='issue',
            name='assignee_user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tasks', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='issue',
            name='author_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='issues', to=settings.AUTH_USER_MODEL),
        ),
    ]