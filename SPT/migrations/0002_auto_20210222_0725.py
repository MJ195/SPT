# Generated by Django 3.1.6 on 2021-02-22 01:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SPT', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='spendings',
            name='detail',
            field=models.CharField(max_length=45),
        ),
    ]
