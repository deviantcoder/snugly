# Generated by Django 5.1.6 on 2025-02-25 14:00

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_mentorprofile_availability_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ManagerProxy',
        ),
        migrations.DeleteModel(
            name='MentorProxy',
        ),
        migrations.DeleteModel(
            name='UserProxy',
        ),
        migrations.CreateModel(
            name='AppUserProxy',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('users.appuser',),
        ),
        migrations.AddField(
            model_name='managerprofile',
            name='bio',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='managerprofile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='mentorprofile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
