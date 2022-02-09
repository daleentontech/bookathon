from datetime import timedelta

from django.utils import timezone
from rest_framework import serializers
from .models import Book


class BookSerializer(serializers.ModelSerializer):
    available_on = serializers.SerializerMethodField()
    days_to_borrow = serializers.SerializerMethodField()
    borrowed_on = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = '__all__'

    def get_available_on(self, obj):
        borrowed_on = obj.borrowed_on
        days_to_borrow = obj.days_to_borrow
        if obj.is_borrowed:
            return borrowed_on + timedelta(days=days_to_borrow)
        return timezone.now()

    def get_days_to_borrow(self, obj):
        return obj.days_to_borrow if obj.is_borrowed else 0

    def get_borrowed_on(self, obj):
        return obj.borrowed_on if obj.is_borrowed else None

    def get_category(self, obj):
        category = obj.category.lower()
        return category if category in ['fiction', 'technology', 'science'] else 'other'


class BookFilterSerializer(serializers.Serializer):
    publisher = serializers.CharField(required=False)
    category = serializers.CharField(required=False)

    def validate_category(self, category):
        category = category.lower()
        return category if category in ['fiction', 'technology', 'science'] else 'other'


class BookBorrowSerializer(serializers.Serializer):
    days_to_borrow = serializers.IntegerField(min_value=1, max_value=30)