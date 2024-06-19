# /words/urls.py
from django.urls import path
from . import views

# Префикс /words/
urlpatterns = [
    path('catalog/', views.CatalogView.as_view(), name='catalog'),  # Общий каталог всех слов
    path('game/', views.GameView.as_view(), name='game'),
    path('flip/', views.FlipCardsView.as_view(), name='flip-cards'),
    path('favorite/<int:id>', views.favorites_word, name='favorites_word'),
    path('speak/<str:word>', views.speak, name='speak'),
    path('save_results/', views.save_results, name='save_results'),
    path('favorites/', views.FavoritesView.as_view(), name='favorites'),  # Общий каталог всех слов d в избранном
    path('learned_words/<int:id>', views.learned_words, name='learned_words'),

]
