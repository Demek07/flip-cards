# Generated by Django 5.0.6 on 2024-06-04 06:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0002_favouriteswords_errors_word'),
    ]

    operations = [
        migrations.AlterField(
            model_name='favouriteswords',
            name='errors_word',
            field=models.IntegerField(db_column='Errors_word', default=0, verbose_name='Количество ошибок'),
        ),
    ]