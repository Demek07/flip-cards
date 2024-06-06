# /cards/urls.py
from django.urls import path
from . import views

# Префикс /cards/
urlpatterns = [
    path('catalog/', views.CatalogView.as_view(), name='catalog'),  # Общий каталог всех карточек
    path('game/', views.GameView.as_view(), name='game'),
    path('flip/', views.FlipCardsView.as_view(), name='flip-cards'),
    path('favorite/<int:id>', views.favourites_word, name='favourites_word'),
    path('speak/<str:word>', views.get_word_audio_url, name='speak'),
]
