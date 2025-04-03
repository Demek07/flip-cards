"""
URL configuration for anki project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from flip_cards import settings
from flip_cards_app import views
from users import views as user_views


# Настраиваем заголовки админ-панели
admin.site.site_header = "Управление моим сайтом"  # Текст в шапке
admin.site.site_title = "Административный сайт"  # Текст в титле
admin.site.index_title = "Добро пожаловать в панель управления"  # Текст на главной странице


# Подключаем файл urls.py из приложения cards через include
urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('', views.IndexView.as_view(), name='index'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('words/', include('flip_cards_app.urls')),
    path('users/', include('users.urls', namespace='users')),
    # path('accounts/', include('allauth.urls')),
    # Профиль / Изменение пароля / Мои карточки
    path("accounts/profile/", user_views.ProfileUser.as_view(), name='profile'),

]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns

    # Добавляем обработку медиафайлов
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Определяем кастомный обработчик 404 ошибки
handler404 = views.PageNotFoundView.as_view()
