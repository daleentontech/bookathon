from django.db import models

# Create your models here.


class Book(models.Model):

    CATEGORY_CHOICES = (
        ('fiction', 'fiction'),
        ('technology', 'technology'),
        ('science', 'science'),
        ('other', 'other'),
    )
    id = models.PositiveIntegerField(primary_key=True)
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