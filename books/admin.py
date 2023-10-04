from django.contrib import admin
from .models import *
# Register your models here.


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = Book.DisplayFields
    search_fields = Book.SearchFields
    list_per_page = 12
    list_max_show_all = 100


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = Genre.DisplayFields
    search_fields = Genre.SearchFields