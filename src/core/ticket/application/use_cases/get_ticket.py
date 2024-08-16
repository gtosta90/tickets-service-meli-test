from dataclasses import dataclass
from datetime import datetime
from uuid import UUID
from src.core.ticket.domain.ticket_repository import TicketRepository
from src.core.ticket.application.use_cases.exceptions import TicketNotFound

from src.core.ticket.domain.ticket import Ticket
from src.core.ticket.domain.value_objects import Level, Status

@dataclass
class GetTicketRequest:
    id: UUID

@dataclass
class GetTicketResponse:
    id: UUID
    title: str
    user_create: int
    category: UUID
    subcategory: UUID
    severity: Level
    description: str
    created_at: datetime
    updated_at: datetime
    user_assigned: int
    status: Status

class GetTicket:
    def __init__(self, repository: TicketRepository):
        self.repository = repository

    def execute(self, request: GetTicketRequest) -> GetTicketResponse:
        ticket = self.repository.get_by_id(request.id)

        if ticket is None:
            raise TicketNotFound(f"Ticket with {request.id} not found")

        return GetTicketResponse(
            id=ticket.id,
            title=ticket.title,
            user_create=ticket.user_create,
            category=ticket.category,
            subcategory=ticket.subcategory,
            severity=ticket.severity,
            description=ticket.description,
            created_at=ticket.created_at,
            updated_at=ticket.updated_at,
            user_assigned=ticket.user_assigned,
            status=ticket.status,
        )