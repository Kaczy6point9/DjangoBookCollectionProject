"""Book_Collection_Managment URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from BooksCollection.views import (
    book_import,
    books_list_view,
    book_import_view, create_book_view)
from .views import (
    home
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', books_list_view),
    re_path(r'^books/?$', books_list_view),
    re_path(r'^Books/(?P<search_term>[A-Z-a-z]+.*)/$', book_import),
    re_path(r'^books/(?P<search_term>[A-Z-a-z]+.*)/$', book_import),
    re_path(r'^books/import/?$', book_import_view),
    re_path(r'^books/create/?$', create_book_view),

]
