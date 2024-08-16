from unittest.mock import create_autospec
import uuid

import pytest
from src.core.ticket.application.use_cases.list_tickets import (
    TicketOutput,
    ListTickets,
    ListTicketsRequest,
    ListTicketsResponse, ListOutputMeta,
)
from src.core.ticket.domain.ticket import Ticket
from src.core.ticket.domain.ticket_repository import TicketRepository
from src.core.ticket.domain.value_objects import Level


class TestListTickets:
    @pytest.fixture
    def ticket_1(self) -> Ticket:
        return Ticket(
            title="Ticket 1",
            description="Ticket 1 Desc",
            user_create=1,
            category=uuid.uuid4(),
            subcategory=None,
            severity=Level.HIGH
        )

    @pytest.fixture
    def ticket_2(self) -> Ticket:
        return Ticket(
            title="Ticket 2",
            description="Ticket 2 Desc",
            user_create=1,
            category=uuid.uuid4(),
            subcategory=None,
            severity=Level.HIGH
        )

    @pytest.fixture
    def ticket_3(self) -> Ticket:
        return Ticket(
            title="Ticket 3",
            description="Ticket 3 Desc",
            user_create=1,
            category=uuid.uuid4(),
            subcategory=None,
            severity=Level.HIGH
        )

    @pytest.fixture
    def mock_empty_repository(self) -> TicketRepository:
        repository = create_autospec(TicketRepository)
        repository.list.return_value = []
        return repository

    @pytest.fixture
    def mock_populated_repository(
        self,
        ticket_1: Ticket,
        ticket_2: Ticket,
        ticket_3: Ticket,
    ) -> TicketRepository:
        repository = create_autospec(TicketRepository)
        repository.list.return_value = [
            ticket_1,
            ticket_2,
            ticket_3
        ]
        return repository

    def test_when_no_tickets_then_return_empty_list(
        self,
        mock_empty_repository: TicketRepository,
    ) -> None:
        use_case = ListTickets(repository=mock_empty_repository)
        response = use_case.execute(request=ListTicketsRequest())

        assert response == ListTicketsResponse(
            data=[],
            meta=ListOutputMeta(
                current_page=1,
                per_page=10,
                total=0,
            ),
        )

    def test_when_ticket_exist_then_return_mapped_list(
        self,
        mock_populated_repository: TicketRepository,
        ticket_1: Ticket,
        ticket_2: Ticket,
        ticket_3: Ticket,
    ) -> None:
        use_case = ListTickets(repository=mock_populated_repository)
        response = use_case.execute(request=ListTicketsRequest())

        assert response == ListTicketsResponse(
            data=[
                TicketOutput(
                    id=ticket_1.id,
                    title=ticket_1.title,
                    user_create=ticket_1.user_create,
                    category=ticket_1.category,
                    subcategory=ticket_1.subcategory,
                    severity=ticket_1.severity,
                    description=ticket_1.description,
                    created_at=ticket_1.created_at,
                    updated_at=ticket_1.updated_at,
                    user_assigned=ticket_1.user_assigned,
                    status=ticket_1.status,
                ),
                TicketOutput(
                    id=ticket_2.id,
                    title=ticket_2.title,
                    user_create=ticket_2.user_create,
                    category=ticket_2.category,
                    subcategory=ticket_2.subcategory,
                    severity=ticket_2.severity,
                    description=ticket_2.description,
                    created_at=ticket_2.created_at,
                    updated_at=ticket_2.updated_at,
                    user_assigned=ticket_2.user_assigned,
                    status=ticket_2.status,
                ),
                TicketOutput(
                    id=ticket_3.id,
                    title=ticket_3.title,
                    user_create=ticket_3.user_create,
                    category=ticket_3.category,
                    subcategory=ticket_3.subcategory,
                    severity=ticket_3.severity,
                    description=ticket_3.description,
                    created_at=ticket_3.created_at,
                    updated_at=ticket_3.updated_at,
                    user_assigned=ticket_3.user_assigned,
                    status=ticket_3.status,
                )
            ],
            meta=ListOutputMeta(
                current_page=1,
                per_page=10,
                total=3,
            ),
        )

    def test_fetch_page_without_elements(self, mock_populated_repository: TicketRepository) -> None:
        use_case = ListTickets(repository=mock_populated_repository)
        response = use_case.execute(request=ListTicketsRequest(current_page=3))

        assert response == ListTicketsResponse(
            data=[],
            meta=ListOutputMeta(
                current_page=3,
                per_page=10,
                total=3,
            ),
        )

    def test_fetch_last_page_with_elements(
        self,
        mock_populated_repository: TicketRepository,
        ticket_3: Ticket,  
    ) -> None:
        use_case = ListTickets(repository=mock_populated_repository)
        response = use_case.execute(request=ListTicketsRequest(current_page=2))

        assert response == ListTicketsResponse(
            data=[],
            meta=ListOutputMeta(
                current_page=2,
                per_page=10,
                total=3,
            ),
        )
