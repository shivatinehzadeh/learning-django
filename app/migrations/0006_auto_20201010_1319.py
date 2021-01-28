# Generated by Django 3.1.1 on 2020-10-10 09:49

import ckeditor_uploader.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_auto_20201010_0856'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to='MyFile/'),
        ),
        migrations.AlterField(
            model_name='book',
            name='description',
            field=ckeditor_uploader.fields.RichTextUploadingField(),
        ),
    ]
