from django.urls import path
from home.views import index, filter_by_genre, sort_by

urlpatterns = [
    path('', index, name='index'),
    path('filter/<genre>/', filter_by_genre, name='filter_by_genre'),
    path('sort_by/<value>/', sort_by, name='sort_by'),
    # path('books/<slug>/', views.get_book, name='get_book'),
]
