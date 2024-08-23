from unittest.mock import MagicMock, create_autospec
from uuid import UUID
import uuid

import pytest
from src.core.category.domain.category import Category
from src.core.category.domain.category_repository import CategoryRepository
from src.core.ticket.domain.ticket_repository import TicketRepository

from src.core.ticket.application.use_cases.get_ticket import GetTicket, GetTicketRequest, GetTicketResponse
from src.core.ticket.application.use_cases.exceptions import TicketNotFound, InvalidTicket
from src.core.ticket.domain.ticket import Ticket
from src.core.ticket.domain.value_objects import Level, Status


class TestGetTicket:
    def test_when_ticket_exists_then_return_response_dto(self):
        
        category = Category(
            name="Teste",
            display_name="Teste"
        )
        
        subcategory = Category(
            name="Teste",
            display_name="Teste",
            relationship_id=category.id
        )

        mock_ticket = Ticket(
            title="Ticket 1",
            description="Ticket 1 Desc",
            user_create=1,
            category=category,
            subcategory=subcategory,
            user_assigned=0,
            severity=Level.HIGH,
            status=1
        )
        
        mock_repository = create_autospec(TicketRepository)
        category_mock_repository = create_autospec(CategoryRepository)

        mock_repository.get_by_id.return_value = mock_ticket
        category_mock_repository.get_by_id.return_value = subcategory
        category_mock_repository.list.return_value = [category, subcategory]

        use_case = GetTicket(ticket_repository=mock_repository, category_repository=category_mock_repository)
        request = GetTicketRequest(id=mock_ticket.id)

        response = use_case.execute(request)

        assert response == GetTicketResponse(
                id=mock_ticket.id,
                title="Ticket 1",
                description="Ticket 1 Desc",
                user_create=mock_ticket.user_create,
                category=mock_ticket.subcategory,
                subcategory=mock_ticket.subcategory,
                severity=Level.HIGH,
                created_at=mock_ticket.created_at,
                updated_at=mock_ticket.updated_at,
                user_assigned=mock_ticket.user_assigned,
                status=1
        )

    def test_when_ticket_not_found_then_raise_exception(self):
        category = Category(
            name="Teste",
            display_name="Teste"
        )
        
        subcategory = Category(
            name="Teste",
            display_name="Teste",
            relationship_id=category.id
        )
    
        mock_repository = create_autospec(TicketRepository)
        category_mock_repository = create_autospec(CategoryRepository)
        
        mock_repository.get_by_id.return_value = None
        category_mock_repository.get_by_id.return_value = subcategory
        category_mock_repository.list.return_value = [category, subcategory]

        use_case = GetTicket(ticket_repository=mock_repository, category_repository=category_mock_repository)
        request = GetTicketRequest(id=uuid.uuid4())

        with pytest.raises(TicketNotFound):
            use_case.execute(request)
