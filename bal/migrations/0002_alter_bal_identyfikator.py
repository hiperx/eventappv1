# Generated by Django 5.0 on 2024-01-08 12:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bal', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bal',
            name='identyfikator',
            field=models.IntegerField(),
        ),
    ]
