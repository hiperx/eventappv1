# Generated by Django 5.0 on 2024-01-26 19:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('piknik', '0002_alter_piknik_przystanek'),
    ]

    operations = [
        migrations.AlterField(
            model_name='piknik',
            name='transport_wlasny',
            field=models.BooleanField(default=True),
        ),
    ]
