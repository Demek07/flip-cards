from datetime import time
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect, JsonResponse
from django.core.cache import cache
from django.db.models import Q
from django.template.defaultfilters import random
from django.views.generic import ListView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from .models import Card
import random
import requests
from soundplay import playsound
# from playsound3 import playsound


info = {
    "menu": [
        {"title": "Главная",
         "url": "/",
         "url_name": "index"},
        {"title": "Словарь",
         "url": "/cards/catalog/",
         "url_name": "catalog"},
        {"title": "Определи слово",
         "url": "/cards/game/",
         "url_name": "game"},
        {"title": "Флип карточки",
         "url": "/cards/flip/",
         "url_name": "flip-cards"},
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

    def get_cards_count(self):
        """
        Возвращает количество карточек из кэша
        return: cards_count - возвращаем количество карточек
        """
        cards_count = cache.get('cards_count')  # получаем количество карточек из кэша
        if not cards_count:  # если количество карточек нет в кэше
            cards_count = Card.objects.count()  # то возвращаем количество карточек
            cache.set('cards_count', cards_count, timeout=self.timeout)  # сохраняем количество карточек в кэше
        return cards_count

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
        context['cards_count'] = self.get_cards_count()  # добавляем в контекст количество карточек
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
    model = Card  # Указываем модель, данные которой мы хотим отобразить
    template_name = 'cards/catalog.html'  # Путь к шаблону, который будет использоваться для отображения страницы
    context_object_name = 'cards'  # Имя переменной контекста, которую будем использовать в шаблоне
    paginate_by = 26  # Количество объектов на странице

    # Метод для модификации начального запроса к БД
    def get_queryset(self):
        # Получение параметров сортировки из GET-запроса
        search_query = self.request.GET.get('search_query', '')
        if search_query:
            queryset = Card.objects.filter(Q(en_word__iexact=search_query) | Q(
                rus_word__iexact=search_query)).order_by('en_word')
        else:
            queryset = Card.objects.all().order_by('en_word')
        return queryset

    def get_context_data(self, **kwargs):
        # Получение существующего контекста из базового класса
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('search_query', '')
        return context


class GameView(MenuMixin, LoginRequiredMixin, ListView):
    model = Card  # Указываем модель, данные которой мы хотим отобразить
    template_name = 'cards/game.html'  # Путь к шаблону, который будет использоваться для отображения страницы
    context_object_name = 'words_game'  # Имя переменной контекста, которую будем использовать в шаблоне

    def get_queryset(self):
        en = []
        rus = []
        en_word = {}
        rus_word = {}
        # all_objects = Card.objects.all()
        all_objects = Card.objects.filter(favourites_word=self.request.user)
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
    model = Card  # Указываем модель, данные которой мы хотим отобразить
    template_name = 'cards/flip_catalog.html'  # Путь к шаблону, который будет использоваться для отображения страницы
    context_object_name = 'flip_cards'  # Имя переменной контекста, которую будем использовать в шаблоне
    paginate_by = 26  # Количество объектов на странице

    # Метод для модификации начального запроса к БД
    def get_queryset(self):
        # Получение параметров сортировки из GET-запроса
        search_query = self.request.GET.get('search_query', '')
        # Фильтрация карточек по поисковому запросу и сортировка
        if search_query:
            queryset = Card.objects.filter(
                Q(en_word__iexact=search_query) | Q(rus_word__iexact=search_query) &
                Q(favourites_word=self.request.user)).order_by('en_word')
        else:
            # Получаем только избранные карточки
            queryset = Card.objects.filter(favourites_word=self.request.user).order_by('en_word')
        return queryset

    def get_context_data(self, **kwargs):
        # Получение существующего контекста из базового класса
        context = super().get_context_data(**kwargs)
        # добавить номер страницы в контекст
        # context['page'] = self.request.GET.get('page')
        # Добавление дополнительных данных в контекст
        # context['sort'] = self.request.GET.get('sort', 'upload_date')
        # context['order'] = self.request.GET.get('order', 'desc')
        context['search_query'] = self.request.GET.get('search_query', '')
        return context


@login_required
def flip_cards(request):
    user = request.user
    cards = user.favourites_word.all()
    context = {
        'flip_cards': cards,
        'menu': info['menu'],
    }
    return render(request, 'cards/flip_catalog.html', context)


# @login_required
# def favourites_word(request, id):
#     card = get_object_or_404(Card, id=id)
#     if card.favourites_word.filter(id=request.user.id).exists():
#         card.favourites_word.remove(request.user)
#     else:
#         card.favourites_word.add(request.user)
    # венуть данные без обновления страницы
    # return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required
def favourites_word(request, id):
    card = get_object_or_404(Card, id=id)
    user = request.user

    if card.favourites_word.filter(id=user.id).exists():
        card.favourites_word.remove(user)
        is_favourite = False
    else:
        card.favourites_word.add(user)
        is_favourite = True

    return JsonResponse({'is_favourite': is_favourite})


def get_word_audio_url(request, word):
    word = word.lower()
    url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
    response = requests.get(url, timeout=10)
    if response.status_code == 200:
        audio_url = response.json()[0]["phonetics"][0]["audio"]
        if audio_url:
            audio_response = requests.get(audio_url, timeout=10)
            if audio_response.status_code == 200:
                # playsound(audio_url)
                playsound(audio_url)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


# def get_word_audio(request):
#     if request.method == 'POST':
#         word = request.POST.get('word')
#         audio_url = get_word_audio_url(word)
#         return JsonResponse({'audio_url': audio_url})
#     return JsonResponse({'audio_url': None})
