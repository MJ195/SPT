# Generated by Django 3.1.6 on 2021-02-22 01:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SPT', '0005_auto_20210222_0658'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shares',
            name='date',
        ),
        migrations.AddField(
            model_name='spendings',
            name='date',
            field=models.DateField(auto_now=True, null=True),
        ),
    ]
