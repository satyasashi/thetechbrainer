# Generated by Django 3.1.2 on 2021-02-12 18:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0007_auto_20201223_0702'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogpost',
            name='banner_image',
            field=models.ImageField(blank=True, upload_to=''),
        ),
    ]