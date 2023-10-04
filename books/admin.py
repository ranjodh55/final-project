from django.contrib import admin
from .models import *
from django.http import HttpResponseRedirect
from django.db import IntegrityError
from django.contrib import messages
# Register your models here.


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = Book.DisplayFields
    search_fields = Book.SearchFields
    list_per_page = 12
    list_max_show_all = 100

    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
        try:
            return super(BookAdmin, self).changeform_view(request, object_id, form_url, extra_context)
        except IntegrityError as e:
            self.message_user(request, e, level=messages.ERROR)
            return HttpResponseRedirect(form_url)


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = Genre.DisplayFields
    search_fields = Genre.SearchFields

    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
        try:
            return super(GenreAdmin, self).changeform_view(request, object_id, form_url, extra_context)
        except IntegrityError as e:
            self.message_user(request, e, level=messages.ERROR)
            return HttpResponseRedirect(form_url)