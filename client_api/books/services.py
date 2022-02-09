from django.db.models import Q
from django.utils import timezone

from .exceptions import ServiceException
from .models import Book


class BookService(object):
    """
    All books related logic are here
    """

    @staticmethod
    def get_book(book_id):
        """Fetch a book by ID"""
        return Book.objects.filter(id=book_id).first()

    @staticmethod
    def retrieve_available_books(filters=None):
        """Retrieve all books"""
        books = Book.objects.filter(is_borrowed=False)

        publisher = filters.get('publisher')
        category = filters.get('category')

        if category and publisher:
            return Book.objects.filter(is_borrowed=False, category=category, publisher=publisher)
        elif category:
            return Book.objects.filter(is_borrowed=False, category=category)
        elif publisher:
            return Book.objects.filter(is_borrowed=False, publisher=publisher)
        else:
            return books

    @staticmethod
    def borrow_book(data=None):
        """Borrow a book"""
        book_id = data.get('book_id')
        days_to_borrow = data.get('days_to_borrow')
        book = BookService.get_book(book_id)
        if book:
            book.is_borrowed = True
            book.days_to_borrow = days_to_borrow
            book.borrowed_on = timezone.now()
            book.save()
            return book
        raise ServiceException("Book not found")