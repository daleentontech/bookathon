from datetime import timedelta

from django.utils import timezone
from rest_framework import serializers
from .models import Book


class BookSerializer(serializers.ModelSerializer):
    available_on = serializers.SerializerMethodField()
    days_to_borrow = serializers.SerializerMethodField()
    borrowed_on = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = '__all__'

    def get_available_on(self, obj):
        borrowed_on = obj.borrowed_on
        days_to_borrow = obj.days_to_borrow
        if obj.is_borrowed:
            return borrowed_on + timedelta(days=days_to_borrow)

    def get_days_to_borrow(self, obj):
        return obj.days_to_borrow if obj.is_borrowed else 0

    def get_borrowed_on(self, obj):
        return obj.borrowed_on if obj.is_borrowed else None


class BookCreateSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=255)
    author = serializers.CharField(max_length=255)
    description = serializers.CharField(max_length=255)
    category = serializers.CharField(max_length=20)
    publisher = serializers.CharField(max_length=255)

    def validate_category(self, category):
        return category.lower()

    def create(self, validated_data):
        return Book.objects.create(**validated_data)

    def update(self, instance, validated_data):
        pass