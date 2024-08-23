from typing import List
from uuid import UUID, uuid4
from core.ticket.domain.ticket_repository import TicketRepository
from core.ticket.domain.ticket import Ticket
from django_project.ticket_app.models import Ticket as TicketORM


class DjangoORMTicketRepository(TicketRepository):
    def __init__(self, model: TicketORM | None = None):
        self.model = model or TicketORM

    def save(self, ticket: Ticket) -> None:
        ticket_model = TicketModelMapper.to_model(ticket)
        ticket_model.save()

    def get_by_id(self, id: UUID) -> Ticket | None:
        try:
            ticket_model = self.model.objects.get(id=id)
            return TicketModelMapper.to_entity(ticket_model)
        except self.model.DoesNotExist:
            return None
         
    def delete(self, id: UUID) -> None:
         self.model.objects.filter(pk=id).delete()
        #self.model.objects.filter(id=id).delete()

    def list(self) -> list[Ticket]:
        return [TicketModelMapper.to_entity(ticket) for ticket in self.model.objects.all()]

    def update(self, ticket: Ticket) -> None:
        self.model.objects.filter(pk=ticket.id).update(
            title=ticket.title,
            category=ticket.category,
            subcategory=ticket.subcategory,
            severity=ticket.severity,
            description=ticket.description,
            user_assigned=ticket.user_assigned,
            status=ticket.status,
            updated_at=ticket.updated_at
        )


class TicketModelMapper:
    @staticmethod
    def to_entity(model: TicketORM) -> Ticket:
        return Ticket(
            id=model.id,
            title=model.title,
            user_create=model.user_create,
            category=model.category,
            subcategory=model.subcategory,
            severity=model.severity,
            description=model.description,
            created_at=model.created_at,
            updated_at=model.updated_at,
            user_assigned=model.user_assigned,
            status=model.status
        )

    @staticmethod
    def to_model(entity: Ticket) -> TicketORM:
        return TicketORM(
            id=entity.id,
            title=entity.title,
            user_create=entity.user_create,
            category=entity.category,
            subcategory=entity.subcategory,
            severity=entity.severity,
            description=entity.description,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
            user_assigned=entity.user_assigned,
            status=entity.status
        )
