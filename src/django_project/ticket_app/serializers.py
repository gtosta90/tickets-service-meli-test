from rest_framework import serializers
from django_project._shared import meta_serializer

class TicketCategorySerializer(serializers.Serializer):
    id = serializers.UUIDField()
    name = serializers.CharField(max_length=255)
    display_name = serializers.CharField(max_length=255)
    relationship_id = serializers.CharField(allow_blank=True, max_length=40)
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()
    is_active = serializers.BooleanField()
    
class TicketResponseSerializer(serializers.Serializer):
    id=serializers.UUIDField()
    title=serializers.CharField(max_length=100)
    user_create=serializers.IntegerField()
    category=TicketCategorySerializer()
    subcategory=TicketCategorySerializer()
    severity=serializers.IntegerField()
    description=serializers.CharField(max_length=1024)
    created_at=serializers.DateTimeField()
    updated_at=serializers.DateTimeField()
    user_assigned=serializers.IntegerField()
    status=serializers.CharField(max_length=40)


class ListTicketsResponseSerializer(serializers.Serializer):
    data = TicketResponseSerializer(many=True)
    meta = meta_serializer.ListOutputMetaSerializer()


class RetrieveTicketRequestSerializer(serializers.Serializer):
    id = serializers.UUIDField()


class RetrieveTicketResponseSerializer(serializers.Serializer):
    data = TicketResponseSerializer(source="*")


class CreateTicketRequestSerializer(serializers.Serializer):
    title=serializers.CharField(max_length=100)
    user_create=serializers.IntegerField()
    category=serializers.UUIDField()
    subcategory=serializers.UUIDField()
    severity=serializers.IntegerField()
    description=serializers.CharField(max_length=1024)
    user_assigned=serializers.IntegerField()
    status=serializers.IntegerField()

class CreateTicketResponseSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    message = serializers.CharField(max_length=1024)


class UpdateTicketRequestSerializer(serializers.Serializer):
    id = serializers.UUIDField(required=True)
    title=serializers.CharField(max_length=100)
    category=serializers.UUIDField()
    subcategory=serializers.UUIDField()
    severity=serializers.IntegerField()
    description=serializers.CharField(max_length=1024)
    user_assigned=serializers.IntegerField()
    status=serializers.IntegerField()

class DeleteTicketRequestSerializer(serializers.Serializer):
    id = serializers.UUIDField()
