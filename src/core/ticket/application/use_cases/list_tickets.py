from abc import ABC
from dataclasses import dataclass, field
from typing import Generic, TypeVar
from uuid import UUID
from datetime import datetime

from src.core.ticket.domain.ticket_repository import TicketRepository
from src.core.ticket.domain.value_objects import Level, Status

@dataclass
class TicketOutput:
    id: UUID
    title: str
    user_create: int
    category: UUID
    severity: Level
    description: str
    created_at: datetime
    updated_at: datetime
    user_assigned: int
    status: Status


@dataclass
class ListTicketsRequest:
    order_by: str = "title"
    current_page: int = 1


@dataclass
class ListOutputMeta:
    current_page: int = 1
    per_page: int = 10
    total: int = 0


T = TypeVar("T")


@dataclass
class ListOutput(Generic[T], ABC):
    data: list[T] = field(default_factory=list)
    meta: ListOutputMeta = field(default_factory=ListOutputMeta)


@dataclass
class ListTicketsResponse(ListOutput[TicketOutput]):
    pass


class ListTickets:
    def __init__(self, repository: TicketRepository) -> None:
        self.repository = repository

    def execute(self, request: ListTicketsRequest) -> ListTicketsResponse:
        tickets = self.repository.list()
        ordered_tickets = sorted(
            tickets,
            key=lambda ticket: getattr(ticket, request.order_by),
        )
        page_offset = (request.current_page - 1) * 2
        tickets_page = ordered_tickets[page_offset:page_offset + 2]

        return ListTicketsResponse(
            data=sorted(
                [
                    TicketOutput(
                        id=ticket.id,
                        title=ticket.title,
                        user_create=ticket.user_create,
                        category=ticket.category,
                        severity=ticket.severity,
                        description=ticket.description,
                        created_at=ticket.created_at,
                        updated_at=ticket.updated_at,
                        user_assigned=ticket.user_assigned,
                        status=ticket.status,
                    ) for ticket in tickets_page
                ],
                key=lambda ticket: getattr(ticket, request.order_by),
            ),
            meta=ListOutputMeta(
                current_page=request.current_page,
                per_page=10,
                total=len(tickets),
            ),
        )
