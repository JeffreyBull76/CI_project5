# Generated by Django 3.2.19 on 2023-06-09 22:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_auto_20230609_2119'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='review',
            name='authorized',
        ),
    ]
