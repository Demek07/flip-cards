# /words/urls.py
from django.urls import path
from . import views

# Префикс /words/
urlpatterns = [
    path('catalog/', views.CatalogView.as_view(), name='catalog'),  # Общий каталог всех слов
    path('game/', views.GameView.as_view(), name='game'),
    path('scramble_game/', views.ScrambleGameView.as_view(), name='scramble_game'),
    path('flip/', views.FlipCardsView.as_view(), name='flip-cards'),
    path('favorite/<int:folder_id>/<int:word_id>', views.favorites_word, name='favorites_word'),
    path('speak/<str:word>', views.speak, name='speak'),
    path('save_results/', views.save_results, name='save_results'),
    path('favorites/', views.FavoriteFolderView.as_view(), name='favorites'),  # Общий каталог всех слов в избранном
    path('learned_words/<int:id>', views.learned_words, name='learned_words'),
    path('catalog/folders/create/', views.FolderCreateView.as_view(), name='create_folder'),
    path('catalog/folders/add/', views.FolderAddWordView.as_view(), name='add_to_folder'),
    path('catalog/folders/remove/', views.FolderRemoveWordView.as_view(), name='remove_from_folder'),
    path('catalog/folders/<int:folder_id>/words/', views.FolderWordsView.as_view(), name='folder_words'),
    path('catalog/folders/rename/', views.RenameFolderView.as_view(), name='rename_folder'),
    path('catalog/folders/delete/', views.DeleteFolderView.as_view(), name='delete_folder'),


]
