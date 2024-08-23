from typing import Any, Self
from rest_framework import serializers
from django_project._shared import meta_serializer

from django_project.category_app.models import Category

class CategoryResponseSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    name = serializers.CharField(max_length=255)
    display_name = serializers.CharField(max_length=255)
    relationship_id = serializers.CharField(allow_blank=True, max_length=40)
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()
    is_active = serializers.BooleanField()

    class Meta:
        model = Category
        fields = ('id', 'name', 'display_name', 'relationship_id', 'created_at', 'updated_at', 'is_active', 'subcategories')

    def get_fields(self):
        fields = super(CategoryResponseSerializer, self).get_fields()
        fields['subcategories'] = CategoryResponseSerializer(many=True)
        return fields

class ListCategoriesResponseSerializer(serializers.Serializer):
    data = CategoryResponseSerializer(many=True)
    meta = meta_serializer.ListOutputMetaSerializer()


class RetrieveCategoryRequestSerializer(serializers.Serializer):
    id = serializers.UUIDField()


class RetrieveCategoryResponseSerializer(serializers.Serializer):
    data = CategoryResponseSerializer(source="*")


class CreateCategoryRequestSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    display_name = serializers.CharField(max_length=255)
    relationship_id = serializers.CharField(allow_blank=True, max_length=40)
    is_active = serializers.BooleanField(default=True)

class CreateCategoryResponseSerializer(serializers.Serializer):
    id = serializers.UUIDField()


class UpdateCategoryRequestSerializer(serializers.Serializer):
    id = serializers.UUIDField(required=True)
    name = serializers.CharField(required=True, max_length=100)
    display_name = serializers.CharField(required=True, max_length=50)
    relationship_id = serializers.CharField(allow_blank=True, max_length=40)
    is_active = serializers.BooleanField(required=True)

class DeleteCategoryRequestSerializer(serializers.Serializer):
    id = serializers.UUIDField()
