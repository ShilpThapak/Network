# Generated by Django 3.1.5 on 2021-02-18 04:17

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0011_auto_20210215_1905'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='likers',
            field=models.ManyToManyField(blank=True, related_name='likedposts', to=settings.AUTH_USER_MODEL),
        ),
    ]
