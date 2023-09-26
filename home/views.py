from django.shortcuts import render
from books.models import Book
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required
def index(request):
    context = {'books': Book.objects.all()}
    return render(request, 'home/index.html',context)