# Generated by Django 3.2.25 on 2024-12-27 00:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0004_auto_20241113_2100'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='num_people',
            field=models.IntegerField(blank=True, null=True, verbose_name='People Count'),
        ),
    ]
