# Generated by Django 3.1.5 on 2021-02-14 12:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0002_post'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='imageurl',
        ),
        migrations.AlterField(
            model_name='post',
            name='likes',
            field=models.IntegerField(blank=True, default='0', null=True),
        ),
    ]
