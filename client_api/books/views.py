from rest_framework.response import Response
from rest_framework.decorators import action

from .producer import publish
from .serializers import BookSerializer, BookFilterSerializer, BookBorrowSerializer
from rest_framework import mixins, permissions, viewsets, status

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

    def get_queryset(self, **filters):
        """Get all available books"""
        queryset = BookService.retrieve_available_books(filters)
        return queryset

    def list(self, request, *args, **kwargs):
        """List all available books and filter by publisher and or category"""
        filters = None
        if self.request.query_params:
            filter_serializer = BookFilterSerializer(data=self.request.query_params)
            if not filter_serializer.is_valid():
                return Response(filter_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            filters = filter_serializer.data
        if filters is not None:
            queryset = self.get_queryset(**filters)
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        query_set = self.get_queryset()
        serializer = self.get_serializer(query_set, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        """Retrieve a single book by ID"""
        try:
            book = BookService.get_book(pk)
        except ServiceException as e:
            return Response(e.message, status=status.HTTP_400_BAD_REQUEST)
        if book is None:
            return Response("Bank not found.", status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(book)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @action(methods=['post'], detail=True, url_path='borrow', url_name='borrow')
    def borrow(self, request, pk=None):
        """Borrow a book by ID"""
        serializer = BookBorrowSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        data = serializer.data
        try:
            data.update({'book_id': pk})
            book = BookService.borrow_book(data)
        except ServiceException as e:
            return Response(e.message, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(book)
        data = {"pk": pk, "is_borrowed": book.is_borrowed, "borrowed_on": book.borrowed_on}
        print(data)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
