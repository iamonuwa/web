# Generated by Django 2.0.3 on 2018-03-29 21:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0049_auto_20180328_0832'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='suppress_leaderboard',
            field=models.BooleanField(default=False, help_text='If this option is chosen, we will remove your profile information from the leaderboard'),
        ),
    ]
