# Generated by Django 3.1.1 on 2020-10-10 05:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='date',
            field=models.ImageField(upload_to=''),
        ),
    ]
