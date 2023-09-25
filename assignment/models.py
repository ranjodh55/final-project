from django.db import models
import uuid
from django.contrib.auth.models import AbstractUser
from django.utils.text import slugify

# Create your models here.
# Each book should have a title, author, genre, price, and available quantity.

class Book(models.Model):
    id = models.UUIDField(primary_key=True, editable=False,default=uuid.uuid4)
    slug = models.SlugField(unique=True, null=True,blank=True)
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    genre = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10,decimal_places=2)
    available_quantity = models.IntegerField()


    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Book, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return self.title

