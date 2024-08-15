import uuid
import pytest
from django_project.ticket_app.repository import DjangoORMTicketRepository
from django_project.ticket_app.models import Ticket as TicketORM
from src.core.ticket.domain.ticket import Ticket


@pytest.mark.django_db
class TestSave:
    def test_save_ticket_in_database(self):
        ticket = Ticket(
            title="Ticket 1",
            user_create=1,
            category=uuid.uuid4(),
            severity=1,
            description="Ticket 1 Desc",
            user_assigned=0,
            status="OPEN",
        )
        repository = DjangoORMTicketRepository()

        assert TicketORM.objects.count() == 0
        repository.save(ticket)
        assert TicketORM.objects.count() == 1
        saved_ticket = TicketORM.objects.get()

        assert saved_ticket.id == ticket.id
