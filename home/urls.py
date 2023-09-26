from django.urls import path
from home.views import index

urlpatterns = [
    path('', index, name='index'),
    # path('books/<slug>/', views.get_book, name='get_book'),
]
