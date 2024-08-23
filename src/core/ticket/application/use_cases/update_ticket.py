
from dataclasses import dataclass
from typing import Set
from uuid import UUID
from core._shared.domain.notification import Notification
from core.category.domain.category_repository import CategoryRepository
from core.user.domain.user_repository import UserRepository
from src.core.ticket.domain.ticket_repository import TicketRepository
from src.core.ticket.application.use_cases.exceptions import RelatedEntitiesNotFound, TicketNotFound, InvalidTicket
from src.core.ticket.domain.value_objects import Level, Status
from src.core.ticket.application.use_cases.validates import Validates

@dataclass
class UpdateTicketRequest:
    id: UUID
    title: str | None = None
    category: UUID | None = None
    subcategory: UUID | None = None
    severity: Level | None = None
    description: str | None = None
    user_assigned: int | None = None
    status: int | None = None

class UpdateTicket:
    def __init__(
                self, 
                ticket_repository: TicketRepository,
                user_repository: UserRepository,
                category_repository: CategoryRepository
            ):
        
        self._ticket_repository = ticket_repository
        self._user_repository = user_repository
        self._category_repository = category_repository

    def execute(self, request: UpdateTicketRequest) -> None:
        notification = Notification()
        validates = Validates()
        notification.add_errors(validates.validate_user_assigned(user_id=request.user_assigned, user_repository=self._user_repository))
        notification.add_errors(validates.validate_category(category_id=request.category, category_repository=self._category_repository))
        notification.add_errors(validates.validate_subcategory(subcategory_id=request.subcategory, category_id=request.category, category_repository=self._category_repository))


        if notification.has_errors:
            raise RelatedEntitiesNotFound(notification.messages)
        
        ticket = self._ticket_repository.get_by_id(request.id)
        if ticket is None:
            raise TicketNotFound(f"Ticket with {request.id} not found")

        try:
            current_title = ticket.title
            current_category = ticket.category
            current_subcategory = ticket.subcategory
            current_severity = ticket.severity
            current_description = ticket.description
            current_user_assigned = ticket.user_assigned
            current_status = ticket.status

            if request.title is not None:
                current_title = request.title

            if request.category is not None:
                current_category = request.category
            
            if request.category is not None:
                current_subcategory = request.subcategory

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
                subcategory=current_subcategory,
                severity=current_severity,
                status=Status(current_status).name
            )
        except ValueError as error:
            raise InvalidTicket(error)

        self._ticket_repository.update(ticket)