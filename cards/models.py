from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model


class Card(models.Model):

    id = models.AutoField(primary_key=True, db_column='ID', verbose_name='ID')
    en_word = models.CharField(max_length=100, db_column='En_word', verbose_name='Слово')
    transcription = models.CharField(max_length=100, db_column='Transcription', verbose_name='Транскрипция')
    rus_word = models.CharField(max_length=100, db_column='Rus_word', verbose_name='Перевод')
    favourites_word = models.ManyToManyField(User, related_name='favourites_word', blank=True)

    class Meta:
        db_table = 'allwords'  # имя таблицы в базе данных
        verbose_name = 'Словарь'  # имя модели в единственном числе
        verbose_name_plural = 'Словари'  # имя модели во множественном числе

    def __str__(self):
        return f'Карточка {self.source} - {self.translations[:10]}'

    # def number_of_favorites_words(self):
    #     if self.favorites_words.count() == 0:
    #         return ''
    #     else:
    #         return self.favorites_words.count()
        
