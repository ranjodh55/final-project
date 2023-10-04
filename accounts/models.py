from django.db import models
from django.contrib.auth.models import User
from base.models import BaseModel
from django.db.models.signals import post_save
from django.dispatch import receiver
import uuid
from base.emails import send_account_activation_email
from books.models import Book
# Create your models here.


class Profile(BaseModel):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='profile')
    is_email_verified = models.BooleanField(default=False)
    email_token = models.CharField(max_length=100, null=True, blank=True)
    forgot_token = models.CharField(max_length=100, null=True, blank=True)

    def get_cart_count(self):
        return CartItems.objects.filter(cart__is_paid = False, cart__user = self.user).count()

class Cart(BaseModel):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='carts')
    is_paid = models.BooleanField(default=False)


    def get_cart_total(self):
        sum = 0
        cart_items = self.cart_items.all()
        for item in cart_items:
            sum += item.get_item_total()
        return sum


class CartItems(BaseModel):
    cart = models.ForeignKey(
        Cart, on_delete=models.CASCADE, related_name='cart_items')
    book = models.ForeignKey(
        Book, on_delete=models.SET_NULL, null=True, blank=True)
<<<<<<< HEAD
    quantity = models.PositiveIntegerField(default=1)

=======
    quantity = models.IntegerField(default=1)
    DisplayFields = ['cart','book','quantity']
    SearchFields = ['cart','book','quantity']
>>>>>>> 60a5ee989bc99803ce5e170d069bbaf7c4aa6c1a

    def get_item_total(self):
        return self.book.price * self.quantity



@receiver(post_save, sender=User)
def send_email_token(sender, instance, created, **kwargs):
    try:
        if created:
            email_token = str(uuid.uuid4())
            Profile.objects.create(user=instance, email_token=email_token)
            email = instance.email
            send_account_activation_email(email, email_token)

    except Exception as e:
        print(e)
