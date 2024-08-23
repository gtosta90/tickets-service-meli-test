from uuid import UUID, uuid4
from django.test import override_settings
from django.urls import reverse
import pytest
from rest_framework import status
from rest_framework.test import APIClient
from src.core.user.domain.user import User

from src.django_project.user_app.repository import ApiClientUserRepository

@pytest.fixture
def user_repository() -> ApiClientUserRepository:
    return ApiClientUserRepository()

class TestListAPI:
    def test_list_users(
        self,
        user_repository: ApiClientUserRepository,
    ) -> None:
        
        url = "/api/users/"
        response = APIClient().get(url)

        assert response.status_code == status.HTTP_403_FORBIDDEN
#         response.data['data'][0]['title'] == expected_data['data'][0]['title']
#         response.data['data'][1]['title'] == expected_data['data'][1]['title']

# @pytest.mark.django_db
# class TestCreateAPI:
#     def test_when_request_data_is_valid_severity_1_then_return_ticket(
#         self,
#         ticket_repository: DjangoORMTicketRepository,
#     ) -> None:
#         url = reverse("ticket-list")
#         data = {
#                     "title": "Ticket 1",
#                     "user_create": uuid4(),
#                     "category": uuid4(),
#                     "severity": 1,
#                     "description": "Ticket 1 Desc",
#                     "user_assigned": "",
#                     "status": "OPEN"
#             }
#         response = APIClient().post(url, data=data)

#         assert response.status_code == status.HTTP_201_CREATED
#         assert response.data["message"]

#     def test_when_request_data_is_valid_then_return_ticket(
#         self,
#         ticket_repository: DjangoORMTicketRepository,
#     ) -> None:
#         url = reverse("ticket-list")
#         data = {
#                     "title": "Ticket 1",
#                     "user_create": uuid4(),
#                     "category": uuid4(),
#                     "severity": 2,
#                     "description": "Ticket 1 Desc",
#                     "user_assigned": "",
#                     "status": "OPEN"
#             }
#         response = APIClient().post(url, data=data)

#         assert response.status_code == status.HTTP_201_CREATED
#         assert response.data["id"]

#         saved_ticket = ticket_repository.get_by_id(response.data["id"])
#         assert saved_ticket.id == UUID(response.data["id"])

# @pytest.mark.django_db
# class TestUpdateAPI:
#     def test_when_request_data_is_valid_then_update_ticket(
#         self,
#         ticket_1: Ticket,
#         ticket_repository: DjangoORMTicketRepository,
#     ) -> None:
#         ticket_repository.save(ticket_1)

#         url = reverse("ticket-detail", kwargs={"pk": ticket_1.id})
    
#         data = {
#             "title": "Ticket 1",
#             "severity": 1,
#             "description": "Ticket 1 Desc",
#             "user_assigned": uuid4(),
#             "status": "IN SERVICE",
#         }
#         response = APIClient().patch(url, data=data)

#         assert response.status_code == status.HTTP_204_NO_CONTENT
#         assert not response.data
#         updated_ticket = ticket_repository.get_by_id(ticket_1.id)
#         assert updated_ticket.title == "Ticket 1"
#         assert updated_ticket.severity == 1
#         assert updated_ticket.description == "Ticket 1 Desc"
#         assert updated_ticket.status == "IN SERVICE"