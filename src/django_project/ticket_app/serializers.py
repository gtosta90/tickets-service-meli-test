from rest_framework import serializers


class TicketResponseSerializer(serializers.Serializer):
    id=serializers.UUIDField()
    title=serializers.CharField(max_length=100)
    user_create=serializers.IntegerField()
    category=serializers.UUIDField(),
    severity=serializers.IntegerField(),
    description=serializers.CharField(max_length=1024),
    created_at=serializers.DateTimeField()
    updated_at=serializers.DateTimeField()
    user_assigned=serializers.IntegerField()
    status=serializers.CharField(max_length=40)

class ListOutputMetaSerializer(serializers.Serializer):
    current_page = serializers.IntegerField()
    per_page = serializers.IntegerField()
    total = serializers.IntegerField()


class ListTicketsResponseSerializer(serializers.Serializer):
    data = TicketResponseSerializer(many=True)
    meta = ListOutputMetaSerializer()


class RetrieveTicketRequestSerializer(serializers.Serializer):
    id = serializers.UUIDField()


class RetrieveTicketResponseSerializer(serializers.Serializer):
    data = TicketResponseSerializer(source="*")


class CreateTicketRequestSerializer(serializers.Serializer):
    title=serializers.CharField(max_length=100)
    user_create=serializers.IntegerField()
    category=serializers.UUIDField()
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
    severity=serializers.IntegerField()
    description=serializers.CharField(max_length=1024)
    user_assigned=serializers.IntegerField()
    status=serializers.CharField(max_length=40)

class DeleteTicketRequestSerializer(serializers.Serializer):
    id = serializers.UUIDField()
