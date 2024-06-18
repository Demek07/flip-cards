from datetime import time
import random
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect, JsonResponse
from django.core.cache import cache
from django.db.models import Q
from django.db import transaction
# from django.template.defaultfilters import random
from django.views.generic import ListView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
import requests
from .models import Word, FavoritesWords


info = {
    "menu": [
        {"title": "Главная",
         "url": "/",
         "url_name": "index"},
        {"title": "Словарь",
         "url": "/words/catalog/",
         "url_name": "catalog"},
        {"title": "Флип карточки",
         "url": "/words/flip/",
         "url_name": "flip-cards"},
        {"title": "Определи слово",
         "url": "/words/game/",
         "url_name": "game"},
        {"title": "Избранное",
         "url": "/words/favorites/",
         "url_name": "favorites"},
        {"title": "О проекте",
         "url": "/about/",
         "url_name": "about"},
    ]
}


class MenuMixin:
    """
    Миксин для вставки меню в шаблон
    """
    timeout = 30  # Время хранения в кэше (в секундах)

    def get_menu(self):
        """
        Возвращает меню из кэша
        return: menu - возвращаем меню
        """
        menu = cache.get('menu')  # получаем меню из кэша
        if not menu:  # если меню нет в кэше
            menu = info['menu']  # то возвращаем меню
            cache.set('menu', menu, timeout=self.timeout)  # сохраняем меню в кэше
        return menu

    def get_words_count(self):
        """
        Возвращает количество карточек из кэша
        return: cards_count - возвращаем количество карточек
        """
        words_count = cache.get('cards_count')  # получаем количество карточек из кэша
        if not words_count:  # если количество карточек нет в кэше
            words_count = Word.objects.count()  # то возвращаем количество карточек
            cache.set('words_count', words_count, timeout=self.timeout)  # сохраняем количество карточек в кэше
        return words_count

    def get_users_count(self):
        """
        Возвращает количество пользователей из кэша
        return: users_count - возвращаем количество пользователей
        """
        users_count = cache.get('users_count')  # получаем количество пользователей из кэша
        if not users_count:  # если количество пользователей нет в кэше
            users_count = get_user_model().objects.count()  # то возвращаем количество пользователей
            cache.set('users_count', users_count, timeout=self.timeout)  # сохраняем количество пользователей в кэше
        return users_count

    def get_context_data(self, **kwargs):
        """
        Метод для модификации контекста для шаблона
        return: context - возвращаем контекст
        """
        context = super().get_context_data(**kwargs)  # вызываем метод родительского класса. Получаем контекст
        context['menu'] = self.get_menu()  # добавляем в контекст меню
        context['cards_count'] = self.get_words_count()  # добавляем в контекст количество карточек
        context['users_count'] = self.get_users_count()  # добавляем в контекст количество пользователей
        return context


class AboutView(MenuMixin, TemplateView):
    """
    Выводим страницу о проекте
    """
    template_name = 'about.html'
    extra_context = {'title': 'О проекте'}


class IndexView(MenuMixin, TemplateView):
    """
    Выводим главную страницу
    """
    template_name = 'main.html'


class PageNotFoundView(MenuMixin, TemplateView):
    template_name = '404.html'


class CatalogView(MenuMixin, ListView):
    """
    Выводим каталог карточек
    """
    model = Word  # Указываем модель, данные которой мы хотим отобразить
    template_name = 'words/catalog.html'  # Путь к шаблону, который будет использоваться для отображения страницы
    context_object_name = 'words'  # Имя переменной контекста, которую будем использовать в шаблоне
    paginate_by = 26  # Количество объектов на странице

    # Метод для модификации начального запроса к БД
    def get_queryset(self):
        # Получение параметров сортировки из GET-запроса
        search_query = self.request.GET.get('search_query', '')
        if search_query:
            queryset = Word.objects.filter(Q(en_word__iregex=search_query) | Q(
                rus_word__iregex=search_query)).order_by('en_word')
        else:
            queryset = Word.objects.all().order_by('en_word')
        return queryset

    def get_context_data(self, **kwargs):
        # Получение существующего контекста из базового класса
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('search_query', '')
        return context


class FavoritesView(MenuMixin, LoginRequiredMixin, ListView):
    """
    Выводим каталог карточек
    """
    model = Word  # Указываем модель, данные которой мы хотим отобразить
    template_name = 'words/catalog.html'  # Путь к шаблону, который будет использоваться для отображения страницы
    context_object_name = 'words'  # Имя переменной контекста, которую будем использовать в шаблоне
    paginate_by = 26  # Количество объектов на странице

    # Метод для модификации начального запроса к БД
    def get_queryset(self):
        # Получение параметров сортировки из GET-запроса
        search_query = self.request.GET.get('search_query', '')
        if search_query:
            queryset = Word.objects.filter(Q(en_word__iregex=search_query) | Q(
                rus_word__iregex=search_query) & Q(favorites_word=self.request.user)).order_by('en_word')
        else:
            queryset = Word.objects.filter(favorites_word=self.request.user).order_by('en_word')
        return queryset

    def get_context_data(self, **kwargs):
        # Получение существующего контекста из базового класса
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('search_query', '')
        return context


class GameView(MenuMixin, LoginRequiredMixin, ListView):
    model = Word  # Указываем модель, данные которой мы хотим отобразить
    template_name = 'words/game.html'  # Путь к шаблону, который будет использоваться для отображения страницы
    context_object_name = 'words_game'  # Имя переменной контекста, которую будем использовать в шаблоне

    def get_queryset(self):
        en = []
        rus = []
        en_word = {}
        rus_word = {}
        # all_objects = Word.objects.all()
        all_objects = Word.objects.filter(favorites_word=self.request.user)
        if all_objects.count() < 10:
            random_objects = random.sample(list(all_objects), all_objects.count())
        else:
            random_objects = random.sample(list(all_objects), 10)
        for item in random_objects:
            en.append((item.id, item.en_word))
            rus.append((item.id, item.rus_word))
        random.shuffle(rus)
        tuple(en)
        tuple(rus)
        en_word = dict(en)
        rus_word = dict(rus)
        return en_word, rus_word

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class FlipCardsView(MenuMixin, LoginRequiredMixin, ListView):
    """
    Выводим каталог карточек
    """
    model = FavoritesWords
  # Указываем модель, данные которой мы хотим отобразить
    template_name = 'words/flip_catalog.html'  # Путь к шаблону, который будет использоваться для отображения страницы
    context_object_name = 'flip_cards'  # Имя переменной контекста, которую будем использовать в шаблоне
    paginate_by = 26  # Количество объектов на странице

    # Метод для модификации начального запроса к БД

    def get_queryset(self):
        # Получение параметров сортировки из GET-запроса
        search_query = self.request.GET.get('search_query', '')

        # Фильтрация карточек по поисковому запросу и сортировка
        if search_query:
            queryset = FavoritesWords.objects.filter(
                Q(card__en_word__iregex=search_query) | Q(card__rus_word__iregex=search_query) &
                Q(user=self.request.user) & Q(is_learned=False)).select_related('word').order_by('word__en_word').distinct()
        else:
            # Получаем только избранные карточки
            queryset = FavoritesWords.objects.filter(Q(user=self.request.user) & Q(
                is_learned=False)).select_related('word').order_by('word__en_word')
        return queryset

    def get_context_data(self, **kwargs):
        # Получение существующего контекста из базового класса
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('search_query', '')
        return context


@login_required
def favorites_word(request, id):
    word = get_object_or_404(Word, id=id)
    user = request.user

    if word.favorites_word.filter(id=user.id).exists():
        word.favorites_word.remove(user)
        is_favorite = False
    else:
        word.favorites_word.add(user)
        is_favorite = True

    return JsonResponse({'is_favorite': is_favorite})


def get_word_audio_url(word):
    url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
    response = requests.get(url, timeout=10)
    if response.status_code == 200:
        audio_url = response.json()[0]["phonetics"][0]["audio"]
        if audio_url:
            return audio_url
    return None


def speak(request, word):
    word = word.lower()
    audio_url = get_word_audio_url(word)
    if audio_url:
        return JsonResponse({'audio_url': audio_url})
    return JsonResponse({'audio_url': None})


@login_required
def save_results(request):
    if request.method == 'POST':
        word = request.POST.get('word_id')
        errors = int(request.POST.get('errors'))
        rights = int(request.POST.get('rights'))
        user = request.user
    with transaction.atomic():
        favorite_word, created = FavoritesWords.objects.get_or_create(
            user=user,
            word=word
        )
        if errors > 0:
            favorite_word.errors_word += errors
        if rights > 0:
            favorite_word.rights_word += rights
        favorite_word.save()


def learned_words(request, id):
    if request.method == 'POST':
        word_id = request.POST.get('word_id')
        is_learned = request.POST.get('is_learned')

        # Обновите или создайте новую запись в модели FavoritesWords
        if is_learned:
            FavoritesWords.objects.filter(id=word_id).update(is_learned=True)

        return JsonResponse({'message': 'Слово помечено как выученное'})
    return JsonResponse({'message': 'Ошибка'}, status=400)
