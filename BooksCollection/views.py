from django.shortcuts import render
import requests
from .models import (
    Book, Author, Category
)

# Create your views here.
def BookImport(request, search_term):

    api_url = 'https://www.googleapis.com/books/v1/volumes?q={}'.format(search_term)
    response = requests.get(api_url)
    json_file = response.json()
    books = json_file['items']

    for book in books:
        book_title = book['volumeInfo']['title']
        qs = Book.objects.filter(book_title=book_title)

        if qs.exists():
            continue

        else:

            obj_Book = Book()
            obj_Book.book_title = book_title
            obj_Book.save()

            for author in book['volumeInfo']["authors"]:
                author_name = author
                qs = Author.objects.filter(author_name=author_name)
                if qs.exists():
                    id = Author.objects.only('id').get(author_name=author_name).id
                    obj_Book.book_authors.add(id)
                else:
                    obj_Author = Author()
                    obj_Author.author_name = author_name
                    obj_Author.save()
                    id = Author.objects.only('id').get(author_name=author_name).id
                    obj_Book.book_authors.add(id)

            if 'categories' in book['volumeInfo'].keys():
                for category in book['volumeInfo']['categories']:
                    category_name = category
                    qs = Category.objects.filter(category_name=category_name)
                    if qs.exists():
                        id = Category.objects.only('id').get(category_name=category_name).id
                        obj_Book.book_categories.add(id)
                    else:
                        obj_Category = Category()
                        obj_Category.category_name = category_name
                        obj_Category.save()
                        id = Category.objects.only('id').get(category_name=category_name).id
                        obj_Book.book_categories.add(id)
            else:
                continue

            if 'description' in book['volumeInfo'].keys():
                obj_Book.book_description = book['volumeInfo']['description']
            else:
                continue
            obj_Book.save()

    return render(request, "home.html")

