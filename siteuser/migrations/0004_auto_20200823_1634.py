# Generated by Django 3.0.8 on 2020-08-23 11:04

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_auto_20200820_0031'),
        ('siteuser', '0003_siteuser_roles'),
    ]

    operations = [
        migrations.AddField(
            model_name='userfollowing',
            name='created_on',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='userfollowing',
            name='updated_on',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='userlikes',
            name='created_on',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='userlikes',
            name='status',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='userlikes',
            name='updated_on',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='userlikes',
            name='blog',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.BlogPost'),
        ),
    ]
