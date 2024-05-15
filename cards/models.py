from django.db import models
from django.contrib.auth import get_user_model

class Card(models.Model):

    id = models.AutoField(primary_key=True, db_column='ID', verbose_name='ID')
    en_word = models.CharField(max_length=100, db_column='En_word', verbose_name='Слово')
    transcription = models.CharField(max_length=100, db_column='Transcription', verbose_name='Транскрипция')
    rus_word = models.CharField(max_length=100, db_column='Rus_word', verbose_name='Перевод')


    class Meta:
        db_table = 'allwords'  # имя таблицы в базе данных
        verbose_name = 'Словарь'  # имя модели в единственном числе
        verbose_name_plural = 'Словари'  # имя модели во множественном числе

    def __str__(self):
        return f'Карточка {self.source} - {self.translations[:10]}'


    # def get_absolute_url(self):
    #     return f'/cards/{self.id}/detail/'



# class Category(models.Model):
#     name = models.CharField(max_length=120, unique=True, db_column='Name', verbose_name='Название')

#     class Meta:
#         verbose_name = 'Категория'
#         verbose_name_plural = 'Категории'

#     def __str__(self):
#         return f'Категория {self.name}'
