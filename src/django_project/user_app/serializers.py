from rest_framework import serializers
from django_project._shared import meta_serializer


class UserResponseSerializer(serializers.Serializer):
    id=serializers.IntegerField()
    name=serializers.CharField()
    username=serializers.CharField()
    email=serializers.CharField()

class ListUsersResponseSerializer(serializers.Serializer):
    data = UserResponseSerializer(many=True)
    meta = meta_serializer.ListOutputMetaSerializer()


class RetrieveUserRequestSerializer(serializers.Serializer):
    id = serializers.IntegerField()


class RetrieveUserResponseSerializer(serializers.Serializer):
    data = UserResponseSerializer(source="*")
