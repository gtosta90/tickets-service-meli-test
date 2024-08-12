from unittest.mock import MagicMock, create_autospec
from uuid import UUID
import uuid

import pytest
from src.core.ticket.domain.ticket_repository import TicketRepository

from src.core.ticket.application.use_cases.get_ticket import GetTicket, GetTicketRequest, GetTicketResponse
from src.core.ticket.application.use_cases.exceptions import TicketNotFound, InvalidTicket
from src.core.ticket.domain.ticket import Ticket
from src.core.ticket.domain.value_objects import Level, Status


class TestGetTicket:
    def test_when_ticket_exists_then_return_response_dto(self):
        mock_category = Ticket(
            title="Ticket 1",
            description="Ticket 1 Desc",
            user_create=uuid.uuid4(),
            category=uuid.uuid4(),
            severity=Level.HIGH,
            status=Status.OPEN
        )
        mock_repository = create_autospec(TicketRepository)
        mock_repository.get_by_id.return_value = mock_category

        use_case = GetTicket(repository=mock_repository)
        request = GetTicketRequest(id=mock_category.id)

        response = use_case.execute(request)

        assert response == GetTicketResponse(
                id=mock_category.id,
                title="Ticket 1",
                user_create=mock_category.user_create,
                category=mock_category.category,
                severity=Level.HIGH,
                description="Ticket 1 Desc",
                created_at=mock_category.created_at,
                updated_at=mock_category.updated_at,
                user_assigned=mock_category.user_assigned,
                status=Status.OPEN
        )

    def test_when_ticket_not_found_then_raise_exception(self):
        mock_repository = create_autospec(TicketRepository)
        mock_repository.get_by_id.return_value = None

        use_case = GetTicket(repository=mock_repository)
        request = GetTicketRequest(id=uuid.uuid4())

        with pytest.raises(TicketNotFound):
            use_case.execute(request)
