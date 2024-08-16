from django.http import QueryDict
from src.django_project.category_app.serializers import CreateCategoryRequestSerializer


class TestCreateCategoryRequestSerializer:
    def test_when_fields_are_valid(self):
        serializer = CreateCategoryRequestSerializer(
            data={
                "name": "KITS",
                "display_name": "KITS",
                "relationship_id": "76151224-4851-4edb-aa79-24a59c5b61e8",
                "is_active": True
            }
        )

        assert serializer.is_valid() is True

    def test_when_is_active_is_not_provided_and_partial_then_do_not_add_it_to_serializer(self):
        serializer = CreateCategoryRequestSerializer(
            data={
                "name": "KITS",
                "display_name": "KITS",
                "relationship_id": "76151224-4851-4edb-aa79-24a59c5b61e8"
            },
            partial=True,
        )

        assert serializer.is_valid() is True
        assert "is_active" not in serializer.validated_data

    def test_when_is_active_is_not_provided_and_not_partial_then_set_to_true(self):
        serializer = CreateCategoryRequestSerializer(
            data={
                "name": "KITS",
                "display_name": "KITS",
                "relationship_id": "76151224-4851-4edb-aa79-24a59c5b61e8"
            },
        )
        assert serializer.is_valid() is True

        assert serializer.validated_data["is_active"] is True
