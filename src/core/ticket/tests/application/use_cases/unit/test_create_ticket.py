from unittest.mock import MagicMock
from uuid import UUID
import uuid

import pytest
from core.category.domain.category import Category
from core.category.domain.category_repository import CategoryRepository
from core.user.domain.user import User
from core.user.domain.user_repository import UserRepository
from src.core.ticket.domain.ticket_repository import TicketRepository

from src.core.ticket.application.use_cases.create_ticket import CreateTicket, CreateTicketRequest, CreateTicketResponse
from src.core.ticket.application.use_cases.exceptions import InvalidTicket
from src.core.ticket.domain.value_objects import Level, Status


class TestCreateTicket:
    def test_create_ticket_with_valid_data(self):
        ticket_mock_repository = MagicMock(TicketRepository)
        category_mock_repository = MagicMock(CategoryRepository)
        user_mock_repository = MagicMock(UserRepository)

        use_case = CreateTicket(
            ticket_repository=ticket_mock_repository,
            category_repository=category_mock_repository,
            user_repository=user_mock_repository,
        )

        user = User(
            id=1,
            name="Teste",
            username="Teste",
            email="teste@teste"
        )

        category = Category(
            name="Teste",
            display_name="Teste"
        )
        
        subcategory = Category(
            name="Teste",
            display_name="Teste",
            relationship_id=category.id
        )

        user_mock_repository.list.return_value = [user]
        category_mock_repository.get_by_id.return_value = subcategory
        category_mock_repository.list.return_value = [category, subcategory]

        request = CreateTicketRequest(
            title="Ticket 1",
            user_create=1,
            category=category.id,
            subcategory=subcategory.id,
            severity=Level.HIGH,
            description="Ticket description",
            user_assigned=1,
            status=1
        )

        response = use_case.execute(request)

        assert response.id is not None
        assert response.message is None
        assert isinstance(response, CreateTicketResponse)
        assert isinstance(response.id, UUID)
        assert ticket_mock_repository.save.called is True

    def test_create_ticket_with_valid_data_and_severity_issue_high(self):
        ticket_mock_repository = MagicMock(TicketRepository)
        category_mock_repository = MagicMock(CategoryRepository)
        user_mock_repository = MagicMock(UserRepository)
        
        use_case = CreateTicket(
            ticket_repository=ticket_mock_repository,
            category_repository=category_mock_repository,
            user_repository=user_mock_repository,
        )
        
        user = User(
            id=1,
            name="Teste",
            username="Teste",
            email="teste@teste"
        )

        category = Category(
            name="Teste",
            display_name="Teste"
        )
        
        subcategory = Category(
            name="Teste",
            display_name="Teste",
            relationship_id=category.id
        )

        user_mock_repository.list.return_value = [user]
        category_mock_repository.get_by_id.return_value = subcategory
        category_mock_repository.list.return_value = [category, subcategory]

        request = CreateTicketRequest(
            title="Ticket 1",
            user_create=1,
            category=category.id,
            subcategory=subcategory.id,
            severity=Level.ISSUE_HIGH,
            description="Ticket description",
            user_assigned=1,
            status=Status.OPEN
        )

        response = use_case.execute(request)

        assert response.id is None
        assert response.message is not None
        assert isinstance(response, CreateTicketResponse)

    def test_create_ticket_with_invalid_data(self):
        ticket_mock_repository = MagicMock(TicketRepository)
        category_mock_repository = MagicMock(CategoryRepository)
        user_mock_repository = MagicMock(UserRepository)
        
        use_case = CreateTicket(
            ticket_repository=ticket_mock_repository,
            category_repository=category_mock_repository,
            user_repository=user_mock_repository,
        )

        user = User(
            id=1,
            name="Teste",
            username="Teste",
            email="teste@teste"
        )

        category = Category(
            name="Teste",
            display_name="Teste"
        )
        
        subcategory = Category(
            name="Teste",
            display_name="Teste",
            relationship_id=category.id
        )

        user_mock_repository.list.return_value = [user]
        category_mock_repository.get_by_id.return_value = subcategory
        category_mock_repository.list.return_value = [category, subcategory]

        with pytest.raises(InvalidTicket, match="title cannot be empty") as exc_info:
            use_case.execute(
                CreateTicketRequest(
                    title="",
                    user_create=1,
                    category=category.id,
                    subcategory=subcategory.id,
                    severity=Level.HIGH,
                    description="Ticket description",
                    user_assigned=1,
                    status=Status.OPEN
                )
            )

        assert exc_info.type is InvalidTicket
        assert str(exc_info.value) == "title cannot be empty"
