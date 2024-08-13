from dataclasses import dataclass
import datetime
from uuid import UUID, uuid4

from src.core.ticket.application.use_cases.exceptions import InvalidTicket
from src.core.ticket.domain.ticket import Ticket
from src.core.ticket.domain.ticket_repository import TicketRepository
from src.core.ticket.domain.value_objects import Level, Status

@dataclass
class CreateTicketRequest:
    title: str
    user_create: UUID
    category: UUID
    severity: Level
    description: str = ""
    user_assigned: UUID = None
    status: Status = Status.OPEN

@dataclass
class CreateTicketResponse:
    id: UUID | None
    message: str

class CreateTicket:
    def __init__(self, repository: TicketRepository):
        self.repository = repository

    def execute(self, request: CreateTicketRequest) -> CreateTicketResponse:
        try:
            if request.severity == 1:
                return CreateTicketResponse(id=None, message="Por favor, crie um ticket no link: http://example/fast, a equipe de guardian buscará resolver a sua issue.")
            
            ticket = Ticket(
                title=request.title,
                user_create=request.user_create,
                category=request.category,
                severity=Level(request.severity),
                description=request.description,
                user_assigned=request.user_assigned,
                status=Status(request.status)
            )
        except ValueError as err:
            raise InvalidTicket(err)

        self.repository.save(ticket)
        return CreateTicketResponse(id=ticket.id, message=None)