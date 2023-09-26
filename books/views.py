from django.shortcuts import render, redirect
from books.models import Book
# Create your views here.


def get_books(request, slug):
    try:
        book = Book.objects.get(slug=slug)
        context = {'book': book}
        return render(request, 'books/books.html', context)
    except Exception as e:
        print(e)
