# Generated by Django 2.2.4 on 2020-04-15 18:55

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0098_auto_20200413_1223'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='ignored_suggested_tribes',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=200), blank=True, default=list, size=None),
        ),
    ]
