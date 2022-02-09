from rest_framework.response import Response
from rest_framework.decorators import action

from .producer import publish
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
        queryset = BookService.retrieve_all_books()
        return queryset

    def create(self, request, *args, **kwargs):
        """
        This endpoint is used to create a new book
        """
        serializer = BookCreateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors)
        data = serializer.validated_data
        try:
            book = BookService.create_book(**data)
        except ServiceException as e:
            return Response(e.message, status=status.HTTP_400_BAD_REQUEST)
        serializer = BookSerializer(book)
        publish("book_created", serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, pk=None):
        try:
            BookService.delete_book(pk)
        except ServiceException as e:
            return Response(e.message, status=status.HTTP_400_BAD_REQUEST)
        publish("book_deleted", pk)
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