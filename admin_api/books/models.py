from django.db import models

# Create your models here.


class Book(models.Model):

    CATEGORY_CHOICES = (
        ('fiction', 'fiction'),
        ('technology', 'technology'),
        ('science', 'science'),
        ('other', 'other'),
    )
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    publisher = models.CharField(max_length=255)
    is_borrowed = models.BooleanField(default=False)
    days_to_borrow = models.PositiveIntegerField(default=0)
    borrowed_on = models.DateTimeField(null=True, blank=True)
    available_on = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class BookUser(models.Model):
    book_id = models.PositiveIntegerField()
    user_id = models.PositiveIntegerField()
    book = models.CharField(max_length=255)
    user = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"book_id-user_id ({self.book_id}-{self.user_id})"


class User(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

    def __str__(self):
        return self.email