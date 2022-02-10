from rest_framework.routers import SimpleRouter
from .views import BooksViewSet, UserViewSet
from django.urls import path, include

book_router = SimpleRouter()
user_router = SimpleRouter()
book_router.register(r'', BooksViewSet, basename='books')
user_router.register(r'', UserViewSet, basename='users')


urlpatterns = [
    path('books/', include(book_router.urls)),
    path('', include(user_router.urls)),
]