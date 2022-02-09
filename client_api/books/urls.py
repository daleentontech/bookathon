from rest_framework.routers import SimpleRouter
from .views import BooksViewSet
from django.urls import path, include

book_router = SimpleRouter()
book_router.register(r'', BooksViewSet, basename='books')


urlpatterns = [
    path('', include(book_router.urls)),
]