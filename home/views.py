from django.shortcuts import render, redirect
from books.models import Book, Genre
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib import messages

# Create your views here.


@login_required
def index(request):
    if request.user.profile.is_email_verified:
        queryset = Book.objects.all()
        search = request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) | Q(author__icontains=search) | Q(genre__icontains=search))
    
        queryset = paginate(request, queryset)
        context = {'books': queryset, 'genres': Genre.objects.all().distinct()}
    else:
        messages.warning(request, 'Email not verified.')
        return redirect('accounts/login/')
    return render(request, 'home/test.html', context)


@login_required
def filter_by_genre(request, genre):
    queryset = Book.objects.filter(genre=genre)
    queryset = paginate(request, queryset)
    context = {'books': queryset, 'genres': Genre.objects.all().distinct()}
    return render(request, 'home/test.html', context)


@login_required
def sort_by(request, value):
    queryset = Book.objects.order_by(value)
    queryset = paginate(request, queryset)
    context = {'books': queryset, 'genres': Genre.objects.all().distinct()}
    return render(request, 'home/test.html', context)


def paginate(request, queryset):
    page = request.GET.get('page', 1)
    paginator = Paginator(queryset, 8)
    try:
        queryset = paginator.get_page(page)
    except PageNotAnInteger:
        queryset = paginator.get_page(1)
    except EmptyPage:
        queryset = paginator.get_page(paginator.num_pages)

    return queryset
