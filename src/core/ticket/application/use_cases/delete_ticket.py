from dataclasses import dataclass
from uuid import UUID
from src.core.ticket.domain.ticket_repository import TicketRepository
from src.core.ticket.application.use_cases.exceptions import TicketNotFound

from src.core.ticket.domain.ticket import Ticket


@dataclass
class DeleteTicketRequest:
    id: UUID

class DeleteTicket:
    def __init__(self, repository: TicketRepository):
        self.repository = repository

    def execute(self, request: DeleteTicketRequest) -> None:
        ticket = self.repository.get_by_id(request.id)

        if ticket is None:
            raise TicketNotFound(f"Ticket with {request.id} not found")

        self.repository.delete(ticket.id)
