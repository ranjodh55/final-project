from django.urls import path
from books.views import get_books

urlpatterns = [
    path('<slug>/', get_books, name='get_books'),
]