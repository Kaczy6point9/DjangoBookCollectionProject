from django.db import models

# Create your models here.

class Author(models.Model):
    author_name = models.CharField(max_length=45)

    def __str__(self):
        return self.author_name

class Category(models.Model):
    category_name = models.CharField(max_length=255)
    class Meta:
        verbose_name_plural = "Categories"
    def __str__(self):
        return self.category_name

class Book(models.Model):
    book_title =  models.CharField(max_length=255)
    book_authors = models.ManyToManyField(Author, blank=True, null=True)
    book_description = models.TextField(null=True, blank=True)
    book_categories = models.ManyToManyField(Category, blank=True, null=True)

    def __str__(self):
        return self.book_title

    @property
    def authors(self):
        return ', '.join([author.author_name for author in self.book_authors.all()])

    def categories(self):
        return ', '.join([category.category_name for category in self.book_categories.all()])