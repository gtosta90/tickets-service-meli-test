from uuid import UUID, uuid4
from django.test import override_settings
from django.urls import reverse
import pytest
from rest_framework import status
from rest_framework.test import APIClient
from core.category.domain.category import Category
from src.core.ticket.domain.ticket import Ticket

from src.django_project.ticket_app.repository import DjangoORMTicketRepository
from src.django_project.category_app.repository import DjangoORMCategoryRepository
from src.django_project.user_app.repository import ApiClientUserRepository


@pytest.fixture
def ticket_1():
    return Ticket(
        title="Ticket 1",
        user_create=1,
        category=uuid4(),
        severity=1,
        description="Ticket 1 Desc",
        user_assigned=0,
        status="OPEN"
    )


@pytest.fixture
def ticket_2():
    return Ticket(
        title="Ticket 2",
        user_create=1,
        category=uuid4(),
        severity=1,
        description="Ticket 2 Desc",
        user_assigned=0,
        status="OPEN"
    )


@pytest.fixture
def ticket_repository() -> DjangoORMTicketRepository:
    return DjangoORMTicketRepository()

@pytest.fixture
def category_repository() -> DjangoORMCategoryRepository:
    return DjangoORMCategoryRepository()

@pytest.fixture
def user_repository() -> ApiClientUserRepository:
    return ApiClientUserRepository()


@pytest.mark.django_db
class TestListAPI:
    def test_list_tickets(
        self,
        ticket_1: Ticket,
        ticket_2: Ticket,
        ticket_repository: DjangoORMTicketRepository,
    ) -> None:
        ticket_repository.save(ticket_1)
        ticket_repository.save(ticket_2)

        url = "/api/tickets/"
        response = APIClient().get(url)

        expected_data = {
            "data": [
                {
                    "id": str(ticket_1.id),
                    "title": "Ticket 1",
                    "user_create": uuid4(),
                    "category": uuid4(),
                    "severity": 1,
                    "description": "Ticket 1 Desc",
                    "user_assigned": None,
                },
                {
                    "id": str(ticket_2.id),
                    "title": "Ticket 2",
                    "user_create": uuid4(),
                    "category": uuid4(),
                    "severity": 1,
                    "description": "Ticket 2 Desc",
                    "user_assigned": None,
                }
            ],
            "meta": {
                "current_page": 1,
                "per_page": 10,
                "total": 2,
            },
        }

        assert response.status_code == status.HTTP_200_OK
        response.data['data'][0]['title'] == expected_data['data'][0]['title']
        response.data['data'][1]['title'] == expected_data['data'][1]['title']

@pytest.mark.django_db
class TestCreateAPI:
    def test_when_request_data_is_valid_severity_1_then_return_ticket(
        self,
        category_repository: DjangoORMCategoryRepository
    ) -> None:
        
        category = Category(
            name= "Teste",
            display_name= "Teste"
        )

        category_repository.save(category=category)

        url = reverse("ticket-list")
        data = {
                    "title": "Ticket 1",
                    "user_create": 1,
                    "category": category.id,
                    "severity": 1,
                    "description": "Ticket 1 Desc",
                    "user_assigned": 1,
                    "status": "OPEN"
            }
        response = APIClient().post(url, data=data)

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["message"]

    def test_when_request_data_is_valid_then_return_ticket(
        self,
        ticket_repository: DjangoORMTicketRepository,
        category_repository: DjangoORMCategoryRepository
    ) -> None:
        
        category = Category(
            name= "Teste",
            display_name= "Teste"
        )

        category_repository.save(category=category)
    
        url = reverse("ticket-list")
        data = {
                    "title": "Ticket 1",
                    "user_create": 1,
                    "category": category.id,
                    "severity": 2,
                    "description": "Ticket 1 Desc",
                    "user_assigned": 0,
                    "status": "OPEN"
            }
        response = APIClient().post(url, data=data)

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["id"]

        saved_ticket = ticket_repository.get_by_id(response.data["id"])
        assert saved_ticket.id == UUID(response.data["id"])

@pytest.mark.django_db
class TestUpdateAPI:
    def test_when_request_data_is_valid_then_update_ticket(
        self,
        ticket_1: Ticket,
        ticket_repository: DjangoORMTicketRepository,
    ) -> None:
        ticket_repository.save(ticket_1)

        url = reverse("ticket-detail", kwargs={"pk": ticket_1.id})
    
        data = {
            "title": "Ticket 1",
            "severity": 1,
            "description": "Ticket 1 Desc",
            "user_assigned": 0,
            "status": "IN SERVICE",
        }
        response = APIClient().patch(url, data=data)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not response.data
        updated_ticket = ticket_repository.get_by_id(ticket_1.id)
        assert updated_ticket.title == "Ticket 1"
        assert updated_ticket.severity == 1
        assert updated_ticket.description == "Ticket 1 Desc"
        assert updated_ticket.status == "IN SERVICE"