# Generated by Django 5.0.6 on 2024-06-24 14:29

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FavoritesWords',
            fields=[
                ('id', models.AutoField(db_column='id', primary_key=True, serialize=False)),
                ('is_learned', models.BooleanField(default=False, verbose_name='Выучено')),
                ('errors_word', models.IntegerField(db_column='Errors_word', default=0, verbose_name='Количество ошибок')),
                ('rights_word', models.IntegerField(db_column='Rights_word', default=0, verbose_name='Количество ответов')),
            ],
            options={
                'verbose_name': 'Избранное слово',
                'verbose_name_plural': 'Избранные слова',
                'db_table': 'FavoritesWords',
            },
        ),
        migrations.CreateModel(
            name='Word',
            fields=[
                ('id', models.AutoField(db_column='ID', primary_key=True, serialize=False, verbose_name='ID')),
                ('en_word', models.CharField(db_column='En_word', max_length=100, verbose_name='Слово')),
                ('transcription', models.CharField(db_column='Transcription', max_length=100, null=True, verbose_name='Транскрипция')),
                ('rus_word', models.CharField(db_column='Rus_word', max_length=100, verbose_name='Перевод')),
                ('img_name_file', models.CharField(db_column='Img_name_file', max_length=100, null=True, verbose_name='Имя файла картинки')),
                ('status', models.BooleanField(choices=[(False, 'Не проверено'), (True, 'Проверено')], default=False, verbose_name='Проверено')),
            ],
            options={
                'verbose_name': 'Словo',
                'verbose_name_plural': 'Слова',
                'db_table': 'allwords',
            },
        ),
    ]
