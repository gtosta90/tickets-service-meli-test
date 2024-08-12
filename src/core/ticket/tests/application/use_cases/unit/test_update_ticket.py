from unittest.mock import create_autospec
import uuid

import pytest
from src.core.ticket.domain.ticket_repository import TicketRepository
from src.core.ticket.application.use_cases.exceptions import TicketNotFound, InvalidTicket
from src.core.ticket.application.use_cases.update_ticket import UpdateTicket, UpdateTicketRequest
from src.core.ticket.domain.ticket import Ticket
from src.core.ticket.domain.value_objects import Level, Status


class TestUpdateTicket:
    @pytest.fixture
    def ticket(self) -> Ticket:
        return Ticket(
            title="Ticket 1",
            description="Ticket 1 Desc",
            user_create=uuid.uuid4(),
            category=uuid.uuid4(),
            severity=Level.HIGH
        )

    @pytest.fixture
    def mock_repository(self, ticket: Ticket) -> TicketRepository:
        repository = create_autospec(TicketRepository, instance=True)
        repository.get_by_id.return_value = ticket
        return repository

    def test_update_category_title_and_description(
        self,
        mock_repository: TicketRepository,
        ticket: Ticket,
    ):
        use_case = UpdateTicket(mock_repository)
        common_uuid = uuid.uuid4()
        use_case.execute(UpdateTicketRequest(
            id=ticket.id,
            title="Ticket 2",
            description="Ticket 2 Desc",
            category=common_uuid,
            severity=Level.MEDIUM,
            user_assigned=common_uuid,
            status=Status.IN_SERVICE
        ))

        assert ticket.title == "Ticket 2"
        assert ticket.description == "Ticket 2 Desc"
        assert ticket.severity == Level.MEDIUM
        assert ticket.status == Status.IN_SERVICE
        assert ticket.category == common_uuid
        assert ticket.user_assigned == common_uuid

        mock_repository.update.assert_called_once_with(ticket)


    def test_when_ticket_is_updated_to_invalid_state_then_raise_exception(
        self,
        mock_repository: TicketRepository,
        ticket: Ticket,
    ) -> None:
        use_case = UpdateTicket(mock_repository)
        request = UpdateTicketRequest(
            id=ticket.id,
            title="",
        )

        with pytest.raises(InvalidTicket) as exc:
            use_case.execute(request)

        mock_repository.update.assert_not_called()
        assert str(exc.value) == "title cannot be empty"
