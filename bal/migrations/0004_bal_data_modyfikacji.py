# Generated by Django 5.0 on 2024-01-18 16:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bal', '0003_alter_bal_identyfikator'),
    ]

    operations = [
        migrations.AddField(
            model_name='bal',
            name='data_modyfikacji',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
