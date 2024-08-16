from unittest.mock import create_autospec
import uuid

import pytest
from core.category.domain.category import Category
from core.category.domain.category_repository import CategoryRepository
from core.user.domain.user import User
from core.user.domain.user_repository import UserRepository
from src.core.ticket.domain.ticket_repository import TicketRepository
from src.core.ticket.application.use_cases.exceptions import TicketNotFound, InvalidTicket
from src.core.ticket.application.use_cases.update_ticket import UpdateTicket, UpdateTicketRequest
from src.core.ticket.domain.ticket import Ticket
from src.core.ticket.domain.value_objects import Level, Status


class TestUpdateTicket:
    
    @pytest.fixture
    def category(self) -> Category:
        return Category(
            name="Teste",
            display_name="Teste"
        )

    @pytest.fixture
    def user(self) -> User:
        return User(
            id=1,
            name="Teste",
            username="Teste",
            email="teste@teste"
        )
    
    @pytest.fixture
    def ticket(self) -> Ticket:
        return Ticket(
            title="Ticket 1",
            description="Ticket 1 Desc",
            user_create=1,
            category=uuid.uuid4(),
            subcategory=None,
            severity=Level.HIGH
        )
    
    @pytest.fixture
    def ticket_mock_repository(self, ticket: Ticket) -> TicketRepository:
        repository = create_autospec(TicketRepository, instance=True)
        repository.get_by_id.return_value = ticket
        return repository
    
    @pytest.fixture
    def category_mock_repository(self, category: Category) -> CategoryRepository:
        repository = create_autospec(CategoryRepository, instance=True)
        repository.list.return_value = [category]
        return repository

    @pytest.fixture
    def user_mock_repository(self, user: User) -> UserRepository:
        repository = create_autospec(UserRepository, instance=True)
        repository.list.return_value = [user]
        return repository
    
    def test_update_category_title_and_description(
        self,
        ticket_mock_repository: TicketRepository,
        category_mock_repository: CategoryRepository,
        user_mock_repository: UserRepository,
        ticket: Ticket,
        category: Category,
        user: User
    ):
        use_case = UpdateTicket(
            ticket_repository=ticket_mock_repository,
            user_repository=user_mock_repository,
            category_repository=category_mock_repository)
        
        ticket.category = category.id

        use_case.execute(UpdateTicketRequest(
            id=ticket.id,
            title="Ticket 2",
            description="Ticket 2 Desc",
            category=category.id,
            subcategory=None,
            severity=Level.MEDIUM,
            user_assigned=user.id,
            status=Status.IN_SERVICE
        ))

        assert ticket.title == "Ticket 2"
        assert ticket.description == "Ticket 2 Desc"
        assert ticket.severity == Level.MEDIUM
        assert ticket.status == Status.IN_SERVICE
        assert ticket.category == category.id
        assert ticket.user_assigned == 1

        ticket_mock_repository.update.assert_called_once_with(ticket)


    def test_when_ticket_is_updated_to_invalid_state_then_raise_exception(
        self,
        ticket_mock_repository: TicketRepository,
        category_mock_repository: CategoryRepository,
        user_mock_repository: UserRepository,
        ticket: Ticket,
        category: Category,
        user: User
    ) -> None:
        use_case = UpdateTicket(
            ticket_repository=ticket_mock_repository,
            user_repository=user_mock_repository,
            category_repository=category_mock_repository)
        
        request = UpdateTicketRequest(
            id=ticket.id,
            title="",
            category=category.id,
            subcategory=None,
            user_assigned=1
        )

        with pytest.raises(InvalidTicket) as exc:
            use_case.execute(request)

        ticket_mock_repository.update.assert_not_called()
        assert str(exc.value) == "title cannot be empty"
