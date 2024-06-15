# /words/urls.py
from django.urls import path
from . import views

# Префикс /words/
urlpatterns = [
    path('catalog/', views.CatalogView.as_view(), name='catalog'),  # Общий каталог всех слов
    path('game/', views.GameView.as_view(), name='game'),
    path('flip/', views.FlipCardsView.as_view(), name='flip-cards'),
    path('favorite/<int:id>', views.favourites_word, name='favourites_word'),
    path('speak/<str:word>', views.speak, name='speak'),
    path('save_results/', views.save_results, name='save_results'),
]
