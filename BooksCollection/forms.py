from django import forms

from BooksCollection.models import Book, Author, Category


class BookAuthorsAndCategoriesSearchForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['book_authors', 'book_categories']

        def clean_book_authors(self):
            return self.cleaned_data['book_authors'] or None

        def clean_book_categories(self):
            return self.cleaned_data['book_categories'] or None


class ImportKeywordsForm(forms.Form):
    keywords = forms.CharField(max_length=255, required=False)


class CreateBookForm(forms.ModelForm):
    authors_names = forms.CharField(max_length=255, required=False, help_text='Write coma separated authors')
    categories_names = forms.CharField(max_length=255, required=False, help_text='Write coma separated categories')

    class Meta:
        model = Book
        fields = ['book_title', 'book_description', 'categories_names', 'authors_names']
