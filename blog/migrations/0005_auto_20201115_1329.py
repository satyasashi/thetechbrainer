# Generated by Django 3.1.2 on 2020-11-15 13:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_remove_blogpost_blog_tags'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='blogpost',
            unique_together={('id', 'blog_slug')},
        ),
    ]
