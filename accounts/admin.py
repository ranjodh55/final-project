from django.contrib import admin
from .models import Profile, Cart, CartItems

# Register your models here.

admin.site.register(Profile)
admin.site.register(Cart)

@admin.register(CartItems)
class CartItemsAdmin(admin.ModelAdmin):
    list_display = CartItems.DisplayFields
    search_fields = CartItems.SearchFields