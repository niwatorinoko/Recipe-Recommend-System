# Generated by Django 3.2.25 on 2024-11-13 11:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('user_ingredients', models.TextField(blank=True, verbose_name='User Ingredients')),
                ('weather', models.CharField(blank=True, max_length=50, verbose_name='Weather')),
                ('mood', models.CharField(blank=True, max_length=50, verbose_name='Mood')),
                ('budget', models.IntegerField(blank=True, null=True, verbose_name='Budget (NTD)')),
                ('num_people', models.IntegerField(blank=True, null=True, verbose_name='Serving Size')),
                ('recipe_info', models.JSONField(blank=True, null=True, verbose_name='Recipe Info')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Author')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
