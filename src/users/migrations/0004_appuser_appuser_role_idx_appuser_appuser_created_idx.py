# Generated by Django 5.1.6 on 2025-02-26 08:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('users', '0003_delete_managerproxy_delete_mentorproxy_and_more'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='appuser',
            index=models.Index(fields=['role'], name='appuser_role_idx'),
        ),
        migrations.AddIndex(
            model_name='appuser',
            index=models.Index(fields=['created'], name='appuser_created_idx'),
        ),
    ]
