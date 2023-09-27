from django.shortcuts import render
from books.models import Book
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required
def index(request):
    context = {'books': Book.objects.filter(available_quantity__gte=1)}
    return render(request, 'home/test.html',context)