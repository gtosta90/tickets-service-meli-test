
from dataclasses import dataclass
from uuid import UUID
from src.core.ticket.domain.ticket_repository import TicketRepository
from src.core.ticket.application.use_cases.exceptions import TicketNotFound, InvalidTicket
from src.core.ticket.domain.value_objects import Level, Status

@dataclass
class UpdateTicketRequest:
    id: UUID
    title: str | None = None
    category: UUID | None = None
    severity: Level | None = None
    description: str | None = None
    user_assigned: UUID | None = None
    status: Status | None = None

class UpdateTicket:
    def __init__(self, repository: TicketRepository):
        self.repository = repository

    def execute(self, request: UpdateTicketRequest) -> None:
        ticket = self.repository.get_by_id(request.id)
        if ticket is None:
            raise TicketNotFound(f"Ticket with {request.id} not found")

        try:
            current_title = ticket.title
            current_category = ticket.category
            current_severity = ticket.severity
            current_description = ticket.description
            current_user_assigned = ticket.user_assigned
            current_status = ticket.status

            if request.title is not None:
                current_title = request.title

            if request.category is not None:
                current_category = request.category

            if request.severity is not None:
                current_severity = request.severity
            
            if request.user_assigned is not None:
                current_user_assigned = request.user_assigned

            if request.status is not None:
                current_status = request.status

            if request.description is not None:
                current_description = request.description

            ticket.update_ticket(
                title=current_title, 
                description=current_description,
                user_assigned=current_user_assigned,
                category=current_category,
                severity=current_severity,
                status=current_status
            )
        except ValueError as error:
            raise InvalidTicket(error)

        self.repository.update(ticket)

