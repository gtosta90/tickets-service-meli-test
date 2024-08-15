from unittest.mock import create_autospec
import uuid

import pytest
from src.core.ticket.domain.ticket_repository import TicketRepository
from src.core.ticket.application.use_cases.delete_ticket import DeleteTicket, DeleteTicketRequest
from src.core.ticket.application.use_cases.exceptions import TicketNotFound
from src.core.ticket.domain.ticket import Ticket
from src.core.ticket.domain.value_objects import Level


class TestDeleteTicket:
    def test_delete_tivket_from_repository(self):
        ticket = Ticket(
            title="Ticket 1",
            user_create=1,
            category=uuid.uuid4(),
            severity=Level.HIGH
        )
        mock_repository = create_autospec(TicketRepository)
        mock_repository.get_by_id.return_value = ticket

        use_case = DeleteTicket(mock_repository)
        use_case.execute(DeleteTicketRequest(id=ticket.id))

        mock_repository.delete.assert_called_once_with(ticket.id)


    def test_when_ticket_not_found_then_raise_exception(self):
        mock_repository = create_autospec(TicketRepository)
        mock_repository.get_by_id.return_value = None

        use_case = DeleteTicket(mock_repository)

        with pytest.raises(TicketNotFound):
            use_case.execute(DeleteTicketRequest(id=uuid.uuid4()))

        mock_repository.delete.assert_not_called()
