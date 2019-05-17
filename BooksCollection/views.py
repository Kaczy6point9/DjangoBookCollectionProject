from django.shortcuts import render
from django.core.paginator import Paginator
import requests
from .models import (
    Book, Author, Category
)

# Create your views here.
def book_import(request, search_term):

    api_url = 'https://www.googleapis.com/books/v1/volumes?q={}'.format(search_term)
    response = requests.get(api_url)
    json_file = response.json()
    books = json_file['items']

    for book in books:
        book_title = book['volumeInfo']['title']
        qs = Book.objects.filter(book_title=book_title)

        if qs.exists():
            continue

        obj_Book = Book()
        obj_Book.book_title = book_title
        obj_Book.save()

        for author_name in book['volumeInfo'].get("authors", []):
            obj, _ = Author.objects.get_or_create(author_name=author_name)
            obj_Book.book_authors.add(obj.id)

        for category_name in book['volumeInfo'].get('categories', []):
            obj, _ = Category.objects.get_or_create(category_name=category_name)
            obj_Book.book_categories.add(obj.id)

        if 'description' in book['volumeInfo'].keys():
            Book.objects.filter(book_title=book_title).update(book_description=book['volumeInfo']['description'])


    return books_list_view(request)

def books_list_view(request):
    book_list = Book.objects.all()
    paginator = Paginator(book_list, 10)
    site_title = 'Books Collection'
    template_name = 'books_collection_list.html'
    page = request.GET.get('page')
    books = paginator.get_page(page)
    context = {'books_list': books, 'title': site_title}

    return render(request, template_name, context)

