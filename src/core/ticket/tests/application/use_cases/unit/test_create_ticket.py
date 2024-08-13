from unittest.mock import MagicMock
from uuid import UUID
import uuid

import pytest
from src.core.ticket.domain.ticket_repository import TicketRepository

from src.core.ticket.application.use_cases.create_ticket import CreateTicket, CreateTicketRequest, CreateTicketResponse
from src.core.ticket.application.use_cases.exceptions import InvalidTicket
from src.core.ticket.domain.value_objects import Level, Status


class TestCreateTicket:
    def test_create_ticket_with_valid_data(self):
        mock_repository = MagicMock(TicketRepository)
        use_case = CreateTicket(repository=mock_repository)
        request = CreateTicketRequest(
            title="Ticket 1",
            user_create=uuid.uuid4(),
            category=uuid.uuid4(),
            severity=Level.HIGH,
            description="Ticket description",
            user_assigned=uuid.uuid4(),
            status=Status.OPEN
        )

        response = use_case.execute(request)

        assert response.id is not None
        assert response.message is None
        assert isinstance(response, CreateTicketResponse)
        assert isinstance(response.id, UUID)
        assert mock_repository.save.called is True

    def test_create_ticket_with_valid_data_and_severity_issue_high(self):
        mock_repository = MagicMock(TicketRepository)
        use_case = CreateTicket(repository=mock_repository)
        request = CreateTicketRequest(
            title="Ticket 1",
            user_create=uuid.uuid4(),
            category=uuid.uuid4(),
            severity=Level.ISSUE_HIGH,
            description="Ticket description",
            user_assigned=uuid.uuid4(),
            status=Status.OPEN
        )

        response = use_case.execute(request)

        assert response.id is None
        assert response.message is not None
        assert isinstance(response, CreateTicketResponse)

    def test_create_ticket_with_invalid_data(self):
        use_case = CreateTicket(repository=MagicMock(TicketRepository))

        with pytest.raises(InvalidTicket, match="title cannot be empty") as exc_info:
            use_case.execute(
                CreateTicketRequest(
                    title="",
                    user_create=uuid.uuid4(),
                    category=uuid.uuid4(),
                    severity=Level.HIGH,
                    description="Ticket description",
                    user_assigned=uuid.uuid4(),
                    status=Status.OPEN
                )
            )

        assert exc_info.type is InvalidTicket
        assert str(exc_info.value) == "title cannot be empty"
