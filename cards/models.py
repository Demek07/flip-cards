from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model


class Card(models.Model):

    id = models.AutoField(primary_key=True, db_column='ID', verbose_name='ID')
    en_word = models.CharField(max_length=100, db_column='En_word', verbose_name='Слово')
    transcription = models.CharField(max_length=100, db_column='Transcription', verbose_name='Транскрипция', null=True)
    rus_word = models.CharField(max_length=100, db_column='Rus_word', verbose_name='Перевод')
    # favourites_word = models.ManyToManyField(User, related_name='favourites_word', blank=True)
    favourites_word = models.ManyToManyField(get_user_model(), through='FavouritesWords',
                                             related_name='cards', verbose_name='Избранные')

    class Meta:
        db_table = 'allwords'  # имя таблицы в базе данных
        verbose_name = 'Словарь'  # имя модели в единственном числе
        verbose_name_plural = 'Словари'  # имя модели во множественном числе

    def __str__(self):
        return f'Карточка {self.source} - {self.translations[:10]}'

    def is_favourited(self, user):
        return user.is_authenticated and self.favourites_word.filter(id=user.id).exists()
    # def number_of_favorites_words(self):
    #     if self.favorites_words.count() == 0:
    #         return ''
    #     else:
    #         return self.favorites_words.count()


class FavouritesWords(models.Model):
    class Learned(models.IntegerChoices):
        UNCHECKED = 0, 'Не выучено'
        CHECKED = 1, 'Выучено'

    id = models.AutoField(primary_key=True, db_column='id')
    card = models.ForeignKey(Card, on_delete=models.CASCADE, db_column='CardID')
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, db_column='UserID')
    is_learned = models.BooleanField(default=False, choices=tuple(
        map(lambda x: (bool(x[0]), x[1]), Learned.choices)), verbose_name='Выучено')
    errors_word = models.IntegerField(default=0, db_column='Errors_word', verbose_name='Количество ошибок')
    rights_word = models.IntegerField(default=0, db_column='Rights_word', verbose_name='Количество ответов')

    class Meta:
        db_table = 'FavouritesWords'
        verbose_name = 'Избранное слово'
        verbose_name_plural = 'Избранные слова'

        # Уникальность пары слово-пользователь
        unique_together = ('card', 'user')
