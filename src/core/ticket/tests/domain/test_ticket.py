import pytest
from uuid import UUID
import uuid

from src.core.ticket.domain.ticket import Ticket
from src.core.ticket.domain.value_objects import Status, Level


class TestTicket:
    def test_title_is_required(self):
        with pytest.raises(
            TypeError, match="missing 1 required positional argument: 'title'"
        ):
            Ticket(user_create=uuid.uuid4(), category=uuid.uuid4(), subcategory=None, severity=Level.ISSUE_HIGH)

    def test_title_must_have_less_than_255_characters(self):
        with pytest.raises(ValueError, match="title cannot be longer than 255"):
            Ticket(title="a" * 256, user_create=uuid.uuid4(), category=uuid.uuid4(), severity=Level.ISSUE_HIGH)

    def test_user_create_is_required(self):
        with pytest.raises(
            TypeError, match="missing 1 required positional argument: 'user_create'"
        ):
            Ticket(title="aaa", category=uuid.uuid4(), severity=Level.ISSUE_HIGH)
    
    def test_category_is_required(self):
        with pytest.raises(
            TypeError, match="missing 1 required positional argument: 'category'"
        ):
            Ticket(title="aaa", user_create=uuid.uuid4(), severity=Level.ISSUE_HIGH)

    def test_severity_is_required(self):
        with pytest.raises(
            TypeError, match="missing 1 required positional argument: 'severity'"
        ):
            Ticket(title="aaa", category=uuid.uuid4(), user_create=uuid.uuid4())



    def test_ticket_must_be_created_with_id_as_uuid_by_default(self):
        ticket = Ticket(title="aaa", category=uuid.uuid4(), user_create=uuid.uuid4(), severity=Level.ISSUE_HIGH)
        assert isinstance(ticket.id, UUID)

    def test_create_ticket_with_default_values(self):
        ticket = Ticket(title="aaa", description="aaaa", category=uuid.uuid4(), user_create=uuid.uuid4(), severity=Level.ISSUE_HIGH, status=Status.OPEN)
        assert ticket.title == "aaa"
        assert ticket.description == "aaaa"
        assert ticket.created_at is not None
        assert ticket.status == "OPEN"

    def test_create_ticket_as_open_by_default(self):
        ticket = Ticket(title="aaa", category=uuid.uuid4(), user_create=uuid.uuid4(), severity=Level.ISSUE_HIGH)
        assert ticket.status == "OPEN"

    def test_create_category_with_provided_values(self):
        ticket_id = uuid.uuid4()
        ticket = Ticket(id=ticket_id, title="aaa", description="aaaa", category=uuid.uuid4(), user_create=uuid.uuid4(), severity=Level.ISSUE_HIGH, status=Status.OPEN)

        assert ticket.id == ticket_id
        assert ticket.title == "aaa"
        assert ticket.description == "aaaa"
        assert ticket.severity == Level.ISSUE_HIGH
        assert ticket.status == Status.OPEN

    def test_cannot_create_ticket_with_empty_title(self):
        with pytest.raises(ValueError, match="title cannot be empty"):
            Ticket(title="", description="aaaa", category=uuid.uuid4(), user_create=uuid.uuid4(), severity=Level.ISSUE_HIGH, status=Status.OPEN)

    def test_cannot_create_ticket_with_description_longer_than_1024(self):
        with pytest.raises(ValueError, match="description cannot be longer than 1024"):
            Ticket(title="aaa", description="a" * 1025, category=uuid.uuid4(), user_create=uuid.uuid4(), severity=Level.ISSUE_HIGH, status=Status.OPEN)

class TestUpdateCategory:
    def test_update_category_with_name_and_display_name(self):
        ticket = Ticket(title="bbb", description="bbbb", category=uuid.uuid4(), subcategory=None, user_create=uuid.uuid4(), severity=Level.ISSUE_HIGH, status=Status.OPEN)
        common_uuid = uuid.uuid4()

        ticket.update_ticket(
            title="bbb", 
            description="bbbb",
            category=common_uuid,
            subcategory=None,
            severity=Level.HIGH,
            user_assigned=common_uuid,
            status=Status.IN_SERVICE,
        )

        assert ticket.title == "bbb"
        assert ticket.description == "bbbb"
        assert ticket.category == common_uuid
        assert ticket.severity == Level.HIGH
        assert ticket.user_assigned == common_uuid
        assert ticket.status == Status.IN_SERVICE


    def test_update_ticket_with_invalid_title_raises_exception(self):
        ticket = Ticket(title="bbb", description="bbbb", category=uuid.uuid4(), user_create=uuid.uuid4(), subcategory=None, severity=Level.ISSUE_HIGH, status=Status.OPEN)

        with pytest.raises(ValueError, match="title cannot be longer than 255"):
            common_uuid = uuid.uuid4()

            ticket.update_ticket(
                title="b" * 256, 
                description="bbbb",
                category=common_uuid,
                subcategory=None,
                severity=Level.HIGH,
                user_assigned=common_uuid,
                status=Status.IN_SERVICE,
            )

    def test_cannot_update_ticket_with_empty_title(self):
        ticket = Ticket(title="bbb", description="bbbb", category=uuid.uuid4(), user_create=uuid.uuid4(), subcategory=None, severity=Level.ISSUE_HIGH, status=Status.OPEN)

        with pytest.raises(ValueError, match="title cannot be empty"):
            common_uuid = uuid.uuid4()

            ticket.update_ticket(
                title="", 
                description="bbbb",
                category=common_uuid,
                subcategory=None,
                severity=Level.HIGH,
                user_assigned=common_uuid,
                status=Status.IN_SERVICE,
            )
            
    def test_update_ticket_with_invalid_description_raises_exception(self):
        ticket = Ticket(title="bbb", description="bbbb", category=uuid.uuid4(), user_create=uuid.uuid4(), subcategory=None, severity=Level.ISSUE_HIGH, status=Status.OPEN)

        with pytest.raises(ValueError, match="description cannot be longer than 1024"):
            common_uuid = uuid.uuid4()

            ticket.update_ticket(
                title="bbb", 
                description="b" * 1025,
                category=common_uuid,
                subcategory=None,
                severity=Level.HIGH,
                user_assigned=common_uuid,
                status=Status.IN_SERVICE,
            )

class TestEquality:
    def test_when_ticket_have_same_id_they_are_equal(self):
        common_id = uuid.uuid4()
        ticket_1 = Ticket(id=common_id, title="bbb", description="bbbb", category=uuid.uuid4(), subcategory=None, user_create=uuid.uuid4(), severity=Level.ISSUE_HIGH, status=Status.OPEN)
        ticket_2 = Ticket(id=common_id, title="bbb", description="bbbb", category=uuid.uuid4(), subcategory=None, user_create=uuid.uuid4(), severity=Level.ISSUE_HIGH, status=Status.OPEN)

        assert ticket_1 == ticket_2

    def test_equality_different_classes(self):
        class Dummy:
            pass

        common_id = uuid.uuid4()
        ticket = Ticket(id=common_id, title="bbb", description="bbbb", category=uuid.uuid4(), subcategory=None, user_create=uuid.uuid4(), severity=Level.ISSUE_HIGH, status=Status.OPEN)
        dummy = Dummy()
        dummy.id = common_id

        assert ticket != dummy
