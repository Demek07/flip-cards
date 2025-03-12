import json
import random
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404, render, redirect
from django.http import JsonResponse, HttpResponseRedirect
from django.core.cache import cache
from django.db.models import Q, Count
from django.db import transaction
from django.views.generic import ListView, TemplateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
import requests
from .models import Word, FavoritesWords, FavoriteFolder
from flip_cards.settings import API_WORDNIK, URL_FOR_VOICE, API_DICTIONARYAPI
from django.urls import reverse_lazy


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
        # {"title": "Определи слово",
        #  "url": "/words/game/",
        #  "url_name": "game"},
        {"title": "Избранное",
         "url": "/words/favorites/",
         "url_name": "favorites"},
        # {"title": "Загрузить слова в избранное",
        #  "url": "/words/load_txt/",
        #  "url_name": "load_txt"},
    ]
}

# Миксин для вставки меню в шаблон


class MenuMixin:
    """
    Миксин для вставки меню в шаблон
    """
    # Время хранения в кэше (в секундах)
    timeout = 30

    def get_menu(self):
        """
        Возвращает меню из кэша
        return: menu - возвращаем меню
        """
        # получаем меню из кэша
        menu = cache.get('menu')
        # если меню нет в кэше
        if not menu:
            # то возвращаем меню
            menu = info['menu']
            # сохраняем меню в кэше
            cache.set('menu', menu, timeout=self.timeout)
        return menu

    # Считаем количество слов
    def get_words_count(self):
        """
        Возвращает количество слов из кэша
        return: cards_count - возвращаем количество слов
        """
        # получаем количество карточек из кэша
        words_count = cache.get('cards_count')
        # если количество карточек нет в кэше
        if not words_count:
            # то возвращаем количество карточек
            words_count = Word.objects.count()
            # сохраняем количество карточек в кэше
            cache.set('words_count', words_count, timeout=self.timeout)
        return words_count

    # Считаем количество пользователей
    def get_users_count(self):
        """
        Возвращает количество пользователей из кэша
        return: users_count - возвращаем количество пользователей
        """
        # получаем количество пользователей из кэша
        users_count = cache.get('users_count')
        # если количество пользователей нет в кэше
        if not users_count:
            # то возвращаем количество пользователей
            users_count = get_user_model().objects.count()
            # сохраняем количество пользователей в кэше
            cache.set('users_count', users_count, timeout=self.timeout)
        return users_count

    # Метод для модификации контекста для шаблона
    def get_context_data(self, **kwargs):
        """
        Метод для модификации контекста для шаблона
        return: context - возвращаем контекст
        """
        # вызываем метод родительского класса. Получаем контекст
        context = super().get_context_data(**kwargs)
        # добавляем в контекст меню
        context['menu'] = self.get_menu()
        # добавляем в контекст количество слов
        context['words_count'] = self.get_words_count()
        # добавляем в контекст количество пользователей
        context['users_count'] = self.get_users_count()
        return context


# Класс для вывода страницы о проекте
class AboutView(MenuMixin, TemplateView):
    """
    Выводим страницу о проекте
    """
    template_name = 'about.html'
    extra_context = {'title': 'О проекте'}


# Класс для вывода главной страницы
class IndexView(MenuMixin, TemplateView):
    """
    Выводим главную страницу
    """
    template_name = 'main.html'


# Класс для вывода страницы 404
class PageNotFoundView(MenuMixin, TemplateView):
    template_name = '404.html'


# Класс для вывода каталога слов
class CatalogView(MenuMixin, ListView):
    """
    Выводим каталог слов
    """
    # Указываем модель, данные которой мы хотим отобразить
    model = Word
    # Путь к шаблону, который будет использоваться для отображения страницы
    template_name = 'words/catalog.html'
    # Имя переменной контекста, которую будем использовать в шаблоне
    context_object_name = 'words'
    # Количество объектов на странице
    paginate_by = 26

    # Метод для модификации начального запроса к БД
    def get_queryset(self):
        # Получение параметров сортировки из GET-запроса
        search_query = self.request.GET.get('search_query', '')
        if search_query:
            queryset = Word.objects.filter(Q(en_word__iregex=search_query) | Q(
                rus_word__iregex=search_query)).order_by('en_word')
        else:
            # queryset = Word.objects.all().order_by('en_word')
            queryset = Word.objects.all().prefetch_related("favorites_word").order_by('en_word')
        return queryset

    def get_context_data(self, **kwargs):
        # Получение существующего контекста из базового класса
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('search_query', '')
        return context


# Класс для вывода каталога избранных слов
class FavoritesView(MenuMixin, LoginRequiredMixin, ListView):
    """
    Выводим каталог избранных слов
    """
    # Указываем модель, данные которой мы хотим отобразить
    model = Word
    # Путь к шаблону, который будет использоваться для отображения страницы
    # template_name = 'words/catalog_favorite.html'
    # Имя переменной контекста, которую будем использовать в шаблоне
    context_object_name = 'words'
    # Количество объектов на странице
    paginate_by = 26

    # Метод для модификации начального запроса к БД
    def get_queryset(self):
        # Получение параметров сортировки из GET-запроса
        search_query = self.request.GET.get('search_query', '')
        # if search_query:
        #     queryset = Word.objects.filter(Q(en_word__iregex=search_query) | Q(
        #         rus_word__iregex=search_query) & Q(favorites_word=self.request.user)).order_by('en_word')
        # else:
        #     queryset = Word.objects.filter(favorites_word=self.request.user).prefetch_related(
        #         "favorites_word").order_by('en_word')
        # return queryset
        # Фильтрация слов по поисковому запросу
        if search_query:
            queryset = FavoritesWords.objects.filter(
                Q(word__en_word__iregex=search_query) | Q(word__rus_word__iregex=search_query) &
                Q(user=self.request.user)).select_related('word').order_by('word__en_word').distinct()
        else:
            # Получаем только избранные слова
            queryset = FavoritesWords.objects.filter(
                user=self.request.user).select_related('word').order_by('word__en_word')
        if queryset.count() > 0:
            self.template_name = 'words/catalog_favorite.html'
        else:
            self.template_name = 'words/empty_favotite.html'
        return queryset

    def get_context_data(self, **kwargs):
        # Получение существующего контекста из базового класса
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('search_query', '')
        return context

    def post(self, request, *args, **kwargs):
        file = request.FILES['file']
        words = file.read().decode('utf-8').splitlines()
        not_found_words = []
        for word in words:
            word = word.strip().lower()
            word_obj = Word.objects.filter(Q(en_word__iexact=word) | Q(rus_word__iexact=word))
            if word_obj.exists():
                for obj in word_obj:
                    print(obj)
                    favorites_word(request, obj.id, load=True)
            else:
                not_found_words.append(word)
        if not_found_words:
            messages.warning(request, f'Следующие слова не загружены: {", ".join(not_found_words)}')
        # context = super().get_context_data(**kwargs)
        # context['search_query'] = self.request.GET.get('search_query', '')
        # return self.render_to_response(context)
        # for word in words:
        #     word = word.strip().lower()
        #     try:
        #         word_obj = Word.objects.filter(Q(en_word__iexact=word) | Q(rus_word__iexact=word))
        #         if word_obj.exists():
        #             for word in word_obj:
        #                 favorites_word(request, word.id, load=True)
        #     except Word.DoesNotExist:
        #         not_found_words.append(word)
        # # context = super().get_context_data(**kwargs)
        # context['search_query'] = self.request.GET.get('search_query', '')
        # context['not_found_words'] = not_found_words
        # return self.render_to_response(context)

        return HttpResponseRedirect(reverse_lazy('favorites'))

        # return render(request, self.template_name, {'not_found_words': not_found_words})


# Класс для вывода страницы игры
class GameView(MenuMixin, LoginRequiredMixin, ListView):
    # Указываем модель, данные которой мы хотим отобразить
    model = Word
    # Имя переменной контекста, которую будем использовать в шаблоне
    context_object_name = 'words_game'

    def get_queryset(self):
        # Обнуляем переменные
        en = []
        rus = []
        en_word = {}
        rus_word = {}
        # Получаем 10 случайных слов
        all_objects = Word.objects.filter(favorites_word=self.request.user)
        if all_objects.count() > 0:
            # Путь к шаблону, который будет использоваться для отображения страницы
            self.template_name = 'words/game.html'
            # Если количество слов меньше 10, то берем все
            if all_objects.count() < 10:
                random_objects = random.sample(list(all_objects), all_objects.count())
            else:
                # Берем 10 случайных слов
                random_objects = random.sample(list(all_objects), 10)
            # Заполняем переменные
            for item in random_objects:
                en.append((item.id, item.en_word))
                rus.append((item.id, item.rus_word))
            # Перемешиваем слова
            random.shuffle(rus)
            tuple(en)
            tuple(rus)
            en_word = dict(en)
            rus_word = dict(rus)
            return en_word, rus_word
        else:
            # Если избранное пусто, то берем шаблон пустого избранного
            self.template_name = 'words/empty_favotite.html'

    # Метод для модификации начального запроса к БД
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


# Класс для вывода страницы игры Word Scramble Game
class ScrambleGameView(MenuMixin, LoginRequiredMixin, ListView):
    # Указываем модель, данные которой мы хотим отобразить
    model = Word
    # Путь к шаблону, который будет использоваться для отображения страницы
    # template_name = 'words/scramble_game.html'
    # Имя переменной контекста, которую будем использовать в шаблоне
    context_object_name = 'scramble_words_game'

    def get_queryset(self):
        # Получаем все слова из избранных слов
        all_objects = Word.objects.filter(favorites_word=self.request.user)
        if all_objects.count() > 0:
            # Если избранное не пусто, то берем шаблон игры
            self.template_name = 'words/scramble_game.html'
            # Берем случайное слово
            random_objects = random.sample(list(all_objects), 1)
            # Заполняем переменные
            en_word = random_objects[0].en_word
            en_word_shuffle = en_word
            rus_word = random_objects[0].rus_word
            hint = random_objects[0].hints.capitalize()
            while en_word.upper() == en_word_shuffle.upper():
                en_word_shuffle = list(en_word.upper())
                # Перемешиваем слова
                random.shuffle(en_word_shuffle)
                en_word_shuffle = ''.join(en_word_shuffle)

            return en_word_shuffle, rus_word, hint, en_word
        else:
            # Если избранное пусто, то берем шаблон пустого избранного
            self.template_name = 'words/empty_favotite.html'
            # return play

    # Метод для модификации начального запроса к БД
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


# Класс для вывода каталога флип карточек
class FlipCardsView(MenuMixin, LoginRequiredMixin, ListView):
    """
    Выводим каталог флип карточек
    """
    # Указываем модель, данные которой мы хотим отобразить
    model = FavoritesWords
    # Путь к шаблону, который будет использоваться для отображения страницы
    # template_name = 'words/flip_catalog.html'
    # Имя переменной контекста, которую будем использовать в шаблоне
    context_object_name = 'flip_cards'
    # Количество объектов на странице
    paginate_by = 26

    # Метод для модификации начального запроса к БД

    def get_queryset(self):
        # Получение параметров сортировки из GET-запроса
        search_query = self.request.GET.get('search_query', '')

        # Фильтрация карточек по поисковому запросу
        if search_query:
            queryset = FavoritesWords.objects.filter(
                Q(word__en_word__iregex=search_query) | Q(word__rus_word__iregex=search_query) &
                Q(user=self.request.user) & Q(is_learned=False)).select_related('word').order_by('word__en_word').distinct()
        else:
            # Получаем только избранные карточки
            queryset = FavoritesWords.objects.filter(Q(user=self.request.user) & Q(
                is_learned=False)).select_related('word').order_by('word__en_word')
        if queryset.count() > 0:
            self.template_name = 'words/flip_catalog.html'
        else:
            self.template_name = 'words/empty_favotite.html'
        return queryset

    def get_context_data(self, **kwargs):
        # Получение существующего контекста из базового класса
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('search_query', '')
        return context


# Метод для добавления/удаления из избранного
@login_required
def favorites_word(request, word_id, folder_id=None, **kwargs):
    word = get_object_or_404(Word, id=word_id)
    user = request.user

    # Проверяем есть ли слово в избранном
    is_favorite = word.favorites_word.filter(id=user.id).exists()

    if is_favorite:
        # Если есть - удаляем
        word.favorites_word.remove(user)
        # Удаляем связанную запись из FavoritesWords
        FavoritesWords.objects.filter(user=user, word=word).delete()
        is_favorite = False
    else:
        # Если нет - добавляем
        # word.favorites_word.add(user)
        # Создаем запись в FavoritesWords
        FavoritesWords.objects.create(
            user=user,
            word=word,
            folder_id=folder_id if folder_id != 'null' else None
        )
        is_favorite = True

    return JsonResponse({'is_favorite': is_favorite})


# Метод для обновления инфы об правильных/неправильных ответах
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
        return JsonResponse({'status': 'success'})


# Метод для изменения статуса - выучено/не выучено
@login_required
def learned_words(request, id):
    if request.method == 'POST':
        word_id = request.POST.get('word_id')
        is_learned = request.POST.get('is_learned')
        is_learned_status = FavoritesWords.objects.get(id=word_id)

        # Обновите или создайте новую запись в модели FavoritesWords
        if is_learned:
            FavoritesWords.objects.filter(id=word_id).update(is_learned=not is_learned_status.is_learned)

        return JsonResponse({'message': 'Слово помечено как выученное'})
    return JsonResponse({'message': 'Ошибка'}, status=400)


# Метод для получения ссылки на аудиофайл слова
def get_word_audio_url(word):
    # Бесплатный API - мало слов
    # url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
    # API Wordnik
    # url = f"https://api.wordnik.com/v4/word.json/{word}/audio?useCanonical=false&limit=1&api_key={API_WORDNIK}"
    # API www.dictionaryapi.com
    url = f"https://www.dictionaryapi.com/api/v3/references/collegiate/json/{word}?key={API_DICTIONARYAPI}"

    response = requests.get(url, timeout=10)
    if response.status_code == 200:
        # получаем ссылку на аудиофайл из бесплтного API
        # audio_url = response.json()[0]["phonetics"][0]["audio"]
        # получаем ссылку на аудиофайл из Wordnik
        # audio_url = response.json()[0]["fileUrl"]
        # получаем ссылку на аудиофайл из www.dictionaryapi.com
        file_name = response.json()[0]['hwi']['prs'][0]['sound']['audio']
        if file_name.startswith('bix'):
            audio_url = f'https://media.merriam-webster.com/audio/prons/en/us/mp3/bix/{file_name}.mp3'
        elif file_name.startswith('gg'):
            audio_url = f'https://media.merriam-webster.com/audio/prons/en/us/mp3/gg/{file_name}.mp3'
        elif file_name.startswith('_'):
            audio_url = f'https://media.merriam-webster.com/audio/prons/en/us/mp3/number/{file_name}.mp3'
        else:
            audio_url = f'https://media.merriam-webster.com/audio/prons/en/us/mp3/{file_name[0]}/{file_name}.mp3'

        if audio_url:
            return audio_url
    return None


# Метод для воспроизведения аудиофайла
def speak(request, word):
    # word = word.lower()
    audio_url = get_word_audio_url(word)
    if audio_url:
        return JsonResponse({'audio_url': audio_url})
    return JsonResponse({'audio_url': None})


class FolderCreateView(View):
    def post(self, request):
        data = json.loads(request.body)
        folder = FavoriteFolder.objects.create(
            name=data['name'],
            user=request.user
        )
        return JsonResponse({'id': folder.id, 'name': folder.name})


class FolderAddWordView(View):
    def post(self, request):
        data = json.loads(request.body)
        word_id = data['word_id']
        folder_id = data['folder_id']

        # Вызываем функцию favorites_word
        response = favorites_word(request, word_id, folder_id)

        return response


class FolderRemoveWordView(View):
    def post(self, request):
        data = json.loads(request.body)
        favorite_word = FavoritesWords.objects.get(
            word_id=data['word_id'],
            user=request.user
        )
        favorite_word.folder = None
        favorite_word.save()
        return JsonResponse({'status': 'success'})


class FavoriteFolderView(MenuMixin, LoginRequiredMixin, ListView):
    model = FavoriteFolder
    template_name = 'words/catalog_favorite_folders.html'
    context_object_name = 'folders'  # это явно укажет имя переменной в шаблоне
    paginate_by = 10

    def get_queryset(self):
        return FavoriteFolder.objects.filter(
            user=self.request.user
        ).annotate(
            words_count=Count('favoriteswords')
        )


class UploadProgressView(View):
    def get(self, request, folder_id):
        progress = cache.get(f'upload_progress_{folder_id}', 0)
        return JsonResponse({'progress': progress})


class FolderWordsView(MenuMixin, LoginRequiredMixin,  ListView):
    template_name = 'words/catalog_favorite_folders_words.html'
    context_object_name = 'words'
    paginate_by = 10

    def get_queryset(self):
        self.folder = get_object_or_404(FavoriteFolder, id=self.kwargs['folder_id'], user=self.request.user)
        return FavoritesWords.objects.filter(
            user=self.request.user,
            folder=self.folder
        ).distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['folder'] = self.folder
        context['total_words'] = self.get_queryset().count()
        return context

    def post(self, request, *args, **kwargs):
        folder_id = self.kwargs['folder_id']

        try:
            if 'file' not in request.FILES:
                messages.error(request, 'Файл не был выбран')
                return JsonResponse({'status': 'error'})

            file = request.FILES['file']

            if not file.name.endswith('.txt'):
                messages.error(request, 'Поддерживаются только .txt файлы')
                return JsonResponse({'status': 'error'})

            try:
                words = file.read().decode('utf-8').splitlines()
                total_words = len(words)
            except UnicodeDecodeError:
                messages.error(request, 'Файл должен быть в кодировке UTF-8')
                return JsonResponse({'status': 'error'})

            not_found_words = []
            added_words = 0
            already_exists = 0

            for i, word in enumerate(words, 1):
                word = word.strip().lower()
                if not word:
                    continue

                word_obj = Word.objects.filter(Q(en_word__iregex=word) | Q(rus_word__iregex=word))

                if word_obj.exists():
                    for obj in word_obj:
                        if not FavoritesWords.objects.filter(user=request.user, word=obj).exists():
                            favorites_word(request, obj.id, folder_id=folder_id, load=True)
                            added_words += 1
                        else:
                            already_exists += 1
                else:
                    not_found_words.append(word)

                progress = (i / total_words) * 100
                cache.set(f'upload_progress_{folder_id}', progress)

            if added_words:
                messages.success(request, f'Успешно добавлено {added_words} слов(а)')

            if already_exists:
                messages.warning(request, f'{already_exists} слов(а) уже были в избранном')

            if not_found_words:
                messages.warning(request, f'Следующие слова не загружены: {", ".join(not_found_words)}')

            return JsonResponse({'status': 'success'})

        except Exception as e:
            messages.error(request, f'Произошла ошибка при загрузке файла: {str(e)}')
            return JsonResponse({'status': 'error'})


class RenameFolderView(View):
    def post(self, request):
        data = json.loads(request.body)
        folder_id = data.get('folder_id')
        new_name = data.get('name')
        folder = get_object_or_404(FavoriteFolder, id=folder_id, user=request.user)
        folder.name = new_name
        folder.save()
        return JsonResponse({'status': 'success'})


class DeleteFolderView(View):
    def post(self, request):
        data = json.loads(request.body)
        folder_id = data.get('folder_id')
        folder = get_object_or_404(FavoriteFolder, id=folder_id, user=request.user)
        folder.delete()
        return JsonResponse({'status': 'success'})
