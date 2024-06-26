from django.contrib import admin
from .models import Word, FavoritesWords
from users.models import User


@admin.register(Word)
class WordsAdmin(admin.ModelAdmin):
    # Поля, которые будут отображаться в админке
    list_display = ('id', 'en_word', 'transcription', 'rus_word', 'status')
    # Поля, которые будут ссылками
    list_display_links = ('id',)
    # Поля по которым будет поиск
    search_fields = ('en_word', 'rus_word')
    # Поля по которым будет фильтрация
    list_filter = ('status',)
    # Ordering - сортировка
    # ordering = ('-upload_date',)
    # List_per_page - количество элементов на странице
    list_per_page = 12
    # Поля, которые можно редактировать
    list_editable = ('status', 'en_word', 'rus_word')
    actions = ['set_checked', 'set_unchecked']
    save_on_top = True
    search_fields = ('rus_word',)
    # изменяем шаблон админки
    # change_form_template = 'admin/cards/change_form_custom.html'

    @admin.action(description="Пометить как проверенное")
    def set_checked(self, request, queryset):
        updated_count = queryset.update(status=Word.Status.CHECKED)
        self.message_user(request, f"{updated_count} записей было помечено как проверенное")

    @admin.action(description="Пометить как непроверенное")
    def set_unchecked(self, request, queryset):
        updated_count = queryset.update(status=Word.Status.UNCHECKED)
        self.message_user(request, f"{updated_count} записей было помечено как непроверенное")


@admin.register(FavoritesWords)
class FavoritesWordsAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_en_word', 'get_transcription', 'get_rus_word',
                    'is_learned', 'errors_word', 'rights_word')
    list_editable = ('is_learned', 'errors_word', 'rights_word',)
    # search_fields = ('name',)
    save_on_top = True

    def get_en_word(self, obj):
        return obj.word.en_word

    get_en_word.short_description = 'Слово'

    def get_transcription(self, obj):
        return obj.word.transcription

    get_transcription.short_description = 'Транскрипция'

    def get_rus_word(self, obj):
        return obj.word.rus_word

    get_rus_word.short_description = 'Перевод'


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'first_name', 'last_name', 'email', 'photo', 'date_birth')
    list_display_links = ('id', 'username')
    save_on_top = True
    search_fields = ('username', 'first_name', 'last_name', 'email')
