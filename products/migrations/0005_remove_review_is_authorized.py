# Generated by Django 3.2.19 on 2023-06-09 22:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_review_is_authorized'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='review',
            name='is_authorized',
        ),
    ]
