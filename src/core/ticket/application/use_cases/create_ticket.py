from dataclasses import dataclass
import datetime
from typing import Set
from uuid import UUID, uuid4
from src import config

from core._shared.domain.notification import Notification
from core.category.domain.category_repository import CategoryRepository
from core.user.domain.user_repository import UserRepository
from src.core.ticket.application.use_cases.exceptions import InvalidTicket, RelatedEntitiesNotFound
from src.core.ticket.domain.ticket import Ticket
from src.core.ticket.domain.ticket_repository import TicketRepository
from src.core.ticket.domain.value_objects import Level, Status
from src.core.ticket.application.use_cases.validates import Validates

@dataclass
class CreateTicketRequest:
    title: str
    user_create: int
    category: UUID
    subcategory: UUID
    severity: Level
    description: str = ""
    user_assigned: int = 0
    status: Status = Status.OPEN

@dataclass
class CreateTicketResponse:
    id: UUID | None
    message: str

class CreateTicket:
    def __init__(
            self, 
            ticket_repository: TicketRepository,
            user_repository: UserRepository,
            category_repository: CategoryRepository
        ):
        self._ticket_repository = ticket_repository
        self._user_repository = user_repository
        self._category_repository = category_repository


    def execute(self, request: CreateTicketRequest) -> CreateTicketResponse:
        notification = Notification()
        validates = Validates()
        notification.add_errors(validates.validate_user(user_id=request.user_create, user_repository=self._user_repository))
        notification.add_errors(validates.validate_user_assigned(user_id=request.user_assigned, user_repository=self._user_repository))
        notification.add_errors(validates.validate_category(category_id=request.category, category_repository=self._category_repository))

        if notification.has_errors:
            raise RelatedEntitiesNotFound(notification.messages)
        
        try:
            if request.severity == 1:
                return CreateTicketResponse(id=None, message=config.MESSAGE_ISSUE_HIGH)
            
            if request.user_assigned == "":
                request.user_assigned = None 
            
            ticket = Ticket(
                title=request.title,
                user_create=request.user_create,
                category=request.category,
                subcategory=request.subcategory,
                severity=Level(request.severity),
                description=request.description,
                user_assigned=request.user_assigned,
                status=Status(request.status)
            )
        except ValueError as err:
            raise InvalidTicket(err)

        self._ticket_repository.save(ticket)
        return CreateTicketResponse(id=ticket.id, message=None)