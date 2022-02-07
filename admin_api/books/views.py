from rest_framework.response import Response
from rest_framework.decorators import action

from .serializers import BookSerializer, BookCreateSerializer
from rest_framework import mixins
from rest_framework import permissions
from rest_framework import status
from rest_framework import viewsets

from .services import BookService
from .exceptions import ServiceException


class BooksViewSet(
        mixins.CreateModelMixin,
        mixins.ListModelMixin,
        mixins.DestroyModelMixin,
        viewsets.GenericViewSet,
        ):
    """
    This view is used to interact with all book specific endpoints
    """

    serializer_class = BookSerializer
    permission_classes = (permissions.AllowAny,)

    def get_queryset(self):
        queryset = BookService.retrive_all_books()
        return queryset

    def create(self, request, *args, **kwargs):
        """
        This endpoint is used to create a new book
        """
        serializer = BookCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # def retrieve(self, request, *args, **kwargs):
    #     """
    #     This endpoint is used to retrieve a book
    #     """
    #     book = BookService.get_book(kwargs.get('pk'))
    #     if book is None:
    #         return Response("Book does not exist", status=status.HTTP_404_NOT_FOUND)
    #     serializer = BookSerializer(book)
    #     return Response(serializer.data)

    def destroy(self, request, *args, pk=None):
        try:
            BookService.delete_book(pk)
        except ServiceException as e:
            return Response(e.message, status=status.HTTP_400_BAD_REQUEST)
        return Response("Book successfully deleted", status=status.HTTP_200_OK)

    @action(methods=["get"], detail=False, url_path="borrowed", url_name="borrowed")
    def borrowed(self, request):
        """
        This endpoint is used to list all books
        """
        books = None
        try:
            books = BookService.retrieve_borrowed_books()
        except ServiceException as e:
            Response(e.message, status=status.HTTP_400_BAD_REQUEST)
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)