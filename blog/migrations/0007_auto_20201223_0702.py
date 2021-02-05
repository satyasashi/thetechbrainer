# Generated by Django 3.1.2 on 2020-12-23 01:32

from django.db import migrations, models
import django.db.models.deletion
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('blog', '0006_auto_20201223_0701'),
    ]

    operations = [
        migrations.CreateModel(
            name='BlogTag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', models.IntegerField(db_index=True, verbose_name='object ID')),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='blog_blogtag_tagged_items', to='contenttypes.contenttype', verbose_name='content type')),
                ('tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='blog_blogtag_items', to='blog.mycustomtag')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.DeleteModel(
            name='BlogTags',
        ),
        migrations.AlterField(
            model_name='blogpost',
            name='blog_tags',
            field=taggit.managers.TaggableManager(blank=True, help_text='A comma-separated list of tags.', through='blog.BlogTag', to='blog.MyCustomTag', verbose_name='Tags'),
        ),
    ]
