# Generated by Django 3.1.2 on 2020-11-02 06:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('siteuser', '0007_auto_20201101_1647'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='personalinformation',
            name='interests',
        ),
        migrations.RemoveField(
            model_name='siteuser',
            name='interests',
        ),
        migrations.RemoveField(
            model_name='siteuser',
            name='roles',
        ),
        migrations.RemoveField(
            model_name='userbookmarks',
            name='blog_post',
        ),
        migrations.RemoveField(
            model_name='userlikes',
            name='blog',
        ),
    ]
