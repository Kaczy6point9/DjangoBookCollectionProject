import urllib
from functools import reduce
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.core.paginator import Paginator
import requests

from BooksCollection.forms import BookAuthorsAndCategoriesSearchForm, ImportKeywordsForm, CreateBookForm
from .models import (
    Book, Author, Category
)


def book_import_view(request):
    template_name = 'import.html'
    site_title = 'Import new books with given keywords'
    keyword_form = ImportKeywordsForm(request.POST or None)
    url = ''
    if keyword_form.is_valid():
        keywords = keyword_form.cleaned_data['keywords'].split(", ")
        for keyword in keywords:
            url += urllib.parse.quote(keyword) + '+'

        return HttpResponseRedirect(url)

    context = {'title': site_title, 'import_form': keyword_form, }

    return render(request, template_name, context)


def book_import(request, search_term):
    print(search_term)
    api_url = 'https://www.googleapis.com/books/v1/volumes?q={}'.format(search_term)
    response = requests.get(api_url)
    json_file = response.json()
    books = json_file['items']

    for book in books:
        book_title = book['volumeInfo']['title']
        qs = Book.objects.filter(book_title=book_title)

        if qs.exists():
            continue

        obj_book = Book()
        obj_book.book_title = book_title
        obj_book.save()

        for author_name in book['volumeInfo'].get("authors", []):
            obj, _ = Author.objects.get_or_create(author_name=author_name)
            obj_book.book_authors.add(obj.id)

        for category_name in book['volumeInfo'].get('categories', []):
            obj, _ = Category.objects.get_or_create(category_name=category_name)
            obj_book.book_categories.add(obj.id)

        if 'description' in book['volumeInfo'].keys():
            Book.objects.filter(book_title=book_title).update(book_description=book['volumeInfo']['description'])

    return books_list_view(request)


def books_list_view(request):
    search_form = BookAuthorsAndCategoriesSearchForm(request.POST or None)

    if search_form.is_valid():
        author_search_param = search_form.cleaned_data['book_authors']
        categories_search_param = search_form.cleaned_data['book_categories']
        url = '?filter&'
        if author_search_param:
            url += 'author='
            for author in author_search_param:
                url += urllib.parse.quote(author.author_name) + '&'
        if categories_search_param:
            url += 'category='
            for category in categories_search_param:
                url += urllib.parse.quote(category.category_name) + '&'
        return HttpResponseRedirect(url)

    if 'filter' in request.GET:
        if "category" in request.GET and "author" in request.GET:
            author_conditions = [
                Q(book_authors__author_name__icontains=author_name)
                for author_name in request.GET.getlist('author')
            ]
            category_conditions = [
                Q(book_categories__category_name__icontains=category_name)
                for category_name in request.GET.getlist('category')
            ]
            book_list = Book.objects.filter(reduce(lambda a, b: a | b, author_conditions) &
                                            reduce(lambda a, b: a | b, category_conditions))

        elif 'author' in request.GET:
            conditions = [
                Q(book_authors__author_name__icontains=author_name)
                for author_name in request.GET.getlist('author')
            ]
            book_list = Book.objects.filter(reduce(lambda a, b: a | b, conditions))

        elif 'category' in request.GET:
            conditions = [
                Q(book_categories__category_name__icontains=category_name)
                for category_name in request.GET.getlist('category')
            ]
            book_list = Book.objects.filter(reduce(lambda a, b: a | b, conditions))
    else:
        book_list = Book.objects.all()

    paginator = Paginator(book_list, 10)
    site_title = 'Books Collection'
    template_name = 'books_collection_list.html'
    page = request.GET.get('page')
    books = paginator.get_page(page)
    context = {'books_list': books, 'title': site_title, 'form': search_form, }

    return render(request, template_name, context)


def create_book_view(request):
    template_name = 'create_book.html'
    site_title = 'Create new book'
    create_book_form = CreateBookForm(request.POST or None)
    if create_book_form.is_valid():
        obj_book = Book()
        obj_book.book_title = create_book_form.cleaned_data['book_title']
        obj_book.save()

        for author_name in create_book_form.cleaned_data['authors_names'].split(", "):
            obj, _ = Author.objects.get_or_create(author_name=author_name)
            obj_book.book_authors.add(obj.id)

        for category_name in create_book_form.cleaned_data['categories_names'].split(", "):
            obj, _ = Category.objects.get_or_create(category_name=category_name)
            obj_book.book_categories.add(obj.id)

        if create_book_form.cleaned_data['book_description']:
            Book.objects.filter(book_title=create_book_form.cleaned_data['book_title']).update(book_description=
                                                                                               create_book_form.cleaned_data['book_description'])

    context = {'title': site_title, 'form': create_book_form, }

    return render(request, template_name, context)
