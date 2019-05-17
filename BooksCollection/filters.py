import django_filters
from django import forms

from .models import Book, Author, Category

class BookFilter(django_filters.FilterSet):
    authors = django_filters.ModelMultipleChoiceFilter(queryset=Author.objects.all(), widget=forms.CheckboxSelectMultiple)
    categories = django_filters.ModelMultipleChoiceFilter(queryset=Category.objects.all(), widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = Book
        fields = ['authors', 'categories']