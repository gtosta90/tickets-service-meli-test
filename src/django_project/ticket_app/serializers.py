from rest_framework import serializers
from django_project._shared import meta_serializer


class TicketResponseSerializer(serializers.Serializer):
    id=serializers.UUIDField()
    title=serializers.CharField(max_length=100)
    user_create=serializers.IntegerField()
    category=serializers.UUIDField()
    subcategory=serializers.UUIDField()
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
    subcategory=serializers.UUIDField(allow_null=True)
    severity=serializers.IntegerField()
    description=serializers.CharField(max_length=1024)
    user_assigned=serializers.IntegerField()
    status=serializers.CharField(max_length=40)

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
    status=serializers.CharField(max_length=40)

class DeleteTicketRequestSerializer(serializers.Serializer):
    id = serializers.UUIDField()
