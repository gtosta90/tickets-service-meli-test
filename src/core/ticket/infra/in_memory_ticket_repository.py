from uuid import UUID
from src.core.ticket.domain.ticket_repository import TicketRepository
from src.core.ticket.domain.ticket import Ticket


class InMemoryTicketRepository(TicketRepository):
    def __init__(self, tickets: list[Ticket]=None):
        self.tickets: list[Ticket] = tickets or []

    def save(self, ticket: Ticket) -> None:
        self.tickets.append(ticket)

    def get_by_id(self, id: UUID) -> Ticket | None:
        return next(
            (ticket for ticket in self.tickets if ticket.id == id), None
        )

    def delete(self, id: UUID) -> None:
        ticket = self.get_by_id(id)
        if ticket:
            self.tickets.remove(ticket)

    def list(self) -> list[Ticket]:
        return [ticket for ticket in self.tickets]

    def update(self, ticket: Ticket) -> None:
        old_ticket = self.get_by_id(ticket.id)
        if old_ticket:
            self.tickets.remove(old_ticket)
            self.tickets.append(ticket)