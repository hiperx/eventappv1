# Generated by Django 5.0 on 2024-01-06 04:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='activeevent',
            options={'verbose_name_plural': 'Active event'},
        ),
        migrations.AlterModelOptions(
            name='oddzial',
            options={'verbose_name_plural': 'Oddzial'},
        ),
    ]
