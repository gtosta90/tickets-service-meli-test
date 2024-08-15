from rest_framework import serializers


class UserResponseSerializer(serializers.Serializer):
    id=serializers.IntegerField()
    name=serializers.CharField()
    username=serializers.CharField()
    email=serializers.CharField()

class ListOutputMetaSerializer(serializers.Serializer):
    current_page = serializers.IntegerField()
    per_page = serializers.IntegerField()
    total = serializers.IntegerField()


class ListUsersResponseSerializer(serializers.Serializer):
    data = UserResponseSerializer(many=True)
    meta = ListOutputMetaSerializer()


class RetrieveUserRequestSerializer(serializers.Serializer):
    id = serializers.IntegerField()


class RetrieveUserResponseSerializer(serializers.Serializer):
    data = UserResponseSerializer(source="*")
