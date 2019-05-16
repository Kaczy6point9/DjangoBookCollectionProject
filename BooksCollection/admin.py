from django.contrib import admin

# Register your models here.
from .models import Author
from .models import Book
from .models import Category

admin.site.register(Book)
admin.site.register(Author)
admin.site.register(Category)