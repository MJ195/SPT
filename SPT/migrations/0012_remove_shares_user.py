# Generated by Django 3.1.6 on 2021-02-28 05:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('SPT', '0011_auto_20210228_1033'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shares',
            name='user',
        ),
    ]
