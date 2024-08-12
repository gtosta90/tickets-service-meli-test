from abc import ABC, abstractmethod
from uuid import UUID

from src.core.ticket.domain.ticket import Ticket


class TicketRepository(ABC):
    @abstractmethod
    def save(self, ticket: Ticket):
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, id: UUID) -> Ticket | None:
        raise NotImplementedError

    @abstractmethod
    def delete(self, id: UUID) -> None:
        raise NotImplementedError

    @abstractmethod
    def list(self) -> list[Ticket]:
        raise NotImplementedError

    @abstractmethod
    def update(self, ticket: Ticket) -> None:
        raise NotImplementedError
