# Generated by Django 3.1.2 on 2020-11-01 20:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_auto_20201101_1704'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogpost',
            name='blog_tags',
            field=models.ManyToManyField(blank=True, to='blog.Tag'),
        ),
    ]
