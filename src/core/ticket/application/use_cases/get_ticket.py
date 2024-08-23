from dataclasses import dataclass
from datetime import datetime
from uuid import UUID
from src.core.category.domain.category import Category
from src.core.ticket.domain.ticket_repository import TicketRepository
from src.core.category.domain.category_repository import CategoryRepository
from src.core.ticket.application.use_cases.exceptions import TicketNotFound

from src.core.ticket.domain.value_objects import Level, Status

@dataclass
class GetTicketRequest:
    id: UUID

@dataclass
class GetTicketResponse:
    id: UUID
    title: str
    user_create: int
    category: Category
    subcategory: Category
    severity: Level
    description: str
    created_at: datetime
    updated_at: datetime
    user_assigned: int
    status: Status

class GetTicket:
    def __init__(self, ticket_repository: TicketRepository, category_repository: CategoryRepository):
        self.ticket_repository = ticket_repository
        self.category_repository = category_repository

    def execute(self, request: GetTicketRequest) -> GetTicketResponse:
        ticket = self.ticket_repository.get_by_id(request.id)
        # import ipdb; ipdb.set_trace()

        if ticket is None:
            raise TicketNotFound(f"Ticket with {request.id} not found")

        return GetTicketResponse(
            id=ticket.id,
            title=ticket.title,
            user_create=ticket.user_create,
            category=self.category_repository.get_by_id(ticket.category),
            subcategory=self.category_repository.get_by_id(ticket.subcategory),
            severity=ticket.severity,
            description=ticket.description,
            created_at=ticket.created_at,
            updated_at=ticket.updated_at,
            user_assigned=ticket.user_assigned,
            status=ticket.status,
        )