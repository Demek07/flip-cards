# Generated by Django 5.0.6 on 2024-06-04 06:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='favouriteswords',
            name='errors_word',
            field=models.IntegerField(default=0),
        ),
    ]
