# Generated by Django 3.2.9 on 2021-11-23 16:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('issues_tracker', '0008_auto_20211123_1628'),
    ]

    operations = [
        migrations.AddField(
            model_name='issue',
            name='priority',
            field=models.CharField(choices=[('Basse', 'Low'), ('Moyenne', 'Average'), ('Elevée', 'High')], default='Moyenne', max_length=10),
        ),
    ]