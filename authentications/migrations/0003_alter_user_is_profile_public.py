# Generated by Django 3.2.25 on 2025-01-07 17:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentications', '0002_user_is_profile_public'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='is_profile_public',
            field=models.BooleanField(default=False, help_text='Is profile public? Indicates whether the user profile is visible to others.'),
        ),
    ]