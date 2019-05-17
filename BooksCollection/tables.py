import django_tables2 as tables
from django_filters.views import FilterView
from django_tables2.views import SingleTableMixin
from .filters import BookFilter

from .models import Book

class BookTable(tables.Table):
    class Meta:
        model = Book
        template_name = 'django_tables2/bootstrap.html'
        fields = ('book_title', 'book_authors', 'book_description','book_categories')

class FilteredBookListView(SingleTableMixin, FilterView):
    table_class = BookTable
    model = Book
    template_name = 'template.html'

    filterset_class = BookFilter
