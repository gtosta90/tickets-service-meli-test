from django.http import QueryDict
from src.django_project.ticket_app.serializers import CreateTicketRequestSerializer


class TestCreateTicketRequestSerializer:
    def test_when_fields_are_valid(self):
        serializer = CreateTicketRequestSerializer(
            data={
                "title": "Ticket 1",
                "user_create": "86bedf25-8628-43a3-a73a-2f3ac051648b",
                "category": "86bedf25-8628-43a3-a73a-2f3ac051648b",
                "severity": 1,
                "description": "Ticket 1 Desc",
                "user_assigned": "",
                "status": "OPEN"
            }
        )

        assert serializer.is_valid() is True

    def test_when_is_active_is_not_provided_and_partial_then_do_not_add_it_to_serializer(self):
        serializer = CreateTicketRequestSerializer(
            data={
                "title": "Ticket 1",
                "user_create": "86bedf25-8628-43a3-a73a-2f3ac051648b",
                "category": "86bedf25-8628-43a3-a73a-2f3ac051648b",
                "severity": 1,
                "description": "Ticket 1 Desc",
                "user_assigned": ""
            },
            partial=True,
        )

        assert serializer.is_valid() is True
        assert "status" not in serializer.validated_data

    def test_when_is_active_is_not_provided_and_not_partial_then_set_to_true(self):
        serializer = CreateTicketRequestSerializer(
            data={
                "title": "Ticket 1",
                "user_create": "86bedf25-8628-43a3-a73a-2f3ac051648b",
                "category": "86bedf25-8628-43a3-a73a-2f3ac051648b",
                "severity": 1,
                "description": "Ticket 1 Desc",
                "user_assigned": "",
                "status": "OPEN"
            },
        )
        assert serializer.is_valid() is True

        assert serializer.validated_data["status"] == "OPEN"
