# Generated by Django 5.0 on 2024-01-26 19:46

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('piknik', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='piknik',
            name='przystanek',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='piknik.przystanek'),
        ),
    ]
