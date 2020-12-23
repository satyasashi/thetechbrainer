# Generated by Django 3.1.2 on 2020-12-23 01:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_blogpost_blog_tags'),
    ]

    operations = [
        migrations.CreateModel(
            name='BlogTags',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='name')),
                ('slug', models.SlugField(max_length=100, unique=True, verbose_name='slug')),
            ],
            options={
                'verbose_name': 'Blog Tag',
                'verbose_name_plural': 'Blog Tags',
            },
        ),
    ]