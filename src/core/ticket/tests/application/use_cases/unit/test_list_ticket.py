from unittest.mock import create_autospec
import uuid

import pytest
from src.core.category.domain.category import Category
from src.core.category.domain.category_repository import CategoryRepository
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
    def mock_category_repository(self) -> CategoryRepository:
        
        category = Category(
            name="Teste",
            display_name="Teste"
        )
        
        subcategory = Category(
            name="Teste",
            display_name="Teste",
            relationship_id=category.id
        )

        repository = create_autospec(CategoryRepository)
        repository.list.return_value = []
        repository.get_by_id.return_value = subcategory
        repository.list.return_value = [category, subcategory]
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
        mock_category_repository: CategoryRepository,
    ) -> None:
        use_case = ListTickets(ticket_repository=mock_empty_repository, category_repository=mock_category_repository)       
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
        mock_category_repository: CategoryRepository,
        ticket_1: Ticket,
        ticket_2: Ticket,
        ticket_3: Ticket,
    ) -> None:
        use_case = ListTickets(ticket_repository=mock_populated_repository, category_repository=mock_category_repository)
        category_mock = mock_category_repository.get_by_id(uuid.uuid4())
        response = use_case.execute(request=ListTicketsRequest())

        assert response == ListTicketsResponse(
            data=[
                TicketOutput(
                    id=ticket_1.id,
                    title=ticket_1.title,
                    user_create=ticket_1.user_create,
                    category=category_mock,
                    subcategory=category_mock,
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
                    category=category_mock,
                    subcategory=category_mock,
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
                    category=category_mock,
                    subcategory=category_mock,
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

    def test_fetch_page_without_elements(
            self, 
            mock_populated_repository: TicketRepository,
            mock_category_repository: CategoryRepository
        ) -> None:
        use_case = ListTickets(ticket_repository=mock_populated_repository, category_repository=mock_category_repository)
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
        mock_category_repository: CategoryRepository,
        ticket_3: Ticket,  
    ) -> None:
        use_case = ListTickets(ticket_repository=mock_populated_repository, category_repository=mock_category_repository)
        response = use_case.execute(request=ListTicketsRequest(current_page=2))

        assert response == ListTicketsResponse(
            data=[],
            meta=ListOutputMeta(
                current_page=2,
                per_page=10,
                total=3,
            ),
        )
