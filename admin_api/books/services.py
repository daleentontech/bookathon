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
    def retrive_all_books():
        """Retrieve all books"""
        return Book.objects.all()

    @staticmethod
    def delete_book(book_id):
        """Delete a book by ID"""
        book_obj = BookService.get_book(book_id)
        if book_obj is None:
            raise ServiceException("Invalid book provided")
        book_obj.delete()

    @staticmethod
    def retrieve_borrowed_books():
        """Retrieve all borrowed books"""
        return Book.objects.filter(is_borrowed=True)