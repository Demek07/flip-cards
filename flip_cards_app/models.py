# dump базы данных - python -Xutf8 manage.py dumpdata --indent=2 > dump.json
# загрузка базы данных - python manage.py loaddata dump.json
from django.db import models
from django.contrib.auth import get_user_model


# Основная модель БД - Слово
class Word(models.Model):
    class Status(models.IntegerChoices):
        UNCHECKED = 0, 'Не проверено'
        CHECKED = 1, 'Проверено'

    id = models.AutoField(primary_key=True, db_column='ID', verbose_name='ID')
    en_word = models.CharField(max_length=100, db_column='En_word', verbose_name='Слово')
    transcription = models.CharField(max_length=100, db_column='Transcription', verbose_name='Транскрипция', null=True)
    rus_word = models.CharField(max_length=100, db_column='Rus_word', verbose_name='Перевод')
    favorites_word = models.ManyToManyField(get_user_model(), through='FavoritesWords',
                                            related_name='favorites_word', verbose_name='Избранные')
    img_name_file = models.CharField(max_length=100, db_column='Img_name_file',
                                     verbose_name='Имя файла картинки', null=True)
    status = models.BooleanField(default=False, choices=tuple(
        map(lambda x: (bool(x[0]), x[1]), Status.choices)), verbose_name='Проверено')

    class Meta:
        db_table = 'allwords'  # имя таблицы в базе данных
        verbose_name = 'Словo'  # имя модели в единственном числе
        verbose_name_plural = 'Слова'  # имя модели во множественном числе

    def is_favorited(self, user):
        return user.is_authenticated and self.favorites_word.filter(id=user.id).exists()


# Модель избранных слов
class FavoritesWords(models.Model):

    id = models.AutoField(primary_key=True, db_column='id')
    word = models.ForeignKey(Word, on_delete=models.CASCADE, db_column='WordID')
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, db_column='UserID')
    is_learned = models.BooleanField(default=False, verbose_name='Выучено')
    errors_word = models.IntegerField(default=0, db_column='Errors_word', verbose_name='Количество ошибок')
    rights_word = models.IntegerField(default=0, db_column='Rights_word', verbose_name='Количество ответов')

    class Meta:
        db_table = 'FavoritesWords'
        verbose_name = 'Избранное слово'
        verbose_name_plural = 'Избранные слова'

        # Уникальность пары слово-пользователь
        unique_together = ('word', 'user')
