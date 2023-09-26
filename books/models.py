from django.db import models
from base.models import BaseModel
from django.utils.text import slugify

# Create your models here.


class Genre(BaseModel):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, null=True, blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Genre, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return self.name


class Book(BaseModel):
    slug = models.SlugField(unique=True, null=True, blank=True)
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    genre = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available_quantity = models.IntegerField()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Book, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return self.title
