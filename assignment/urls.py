from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('home/', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('books/<slug>/', views.get_book, name='get_book'),
    path('logout/', views.logout_user, name='logout_user'),
    path('login/', views.login_user, name='login_user'),
]
