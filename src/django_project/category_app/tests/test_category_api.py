from uuid import UUID, uuid4
from django.test import override_settings
from django.urls import reverse
import pytest
from rest_framework import status
from rest_framework.test import APIClient
from src.core.category.domain.category import Category

from src.django_project.category_app.repository import DjangoORMCategoryRepository

@pytest.fixture
def category_1():
    return Category(
        name="KITS",
        display_name="KITS",
        relationship_id="",
        is_active= True
    )


@pytest.fixture
def category_2():
    return Category(
        name="KITS1",
        display_name="KITS1",
        relationship_id="76151224-4851-4edb-aa79-24a59c5b61e8",
        is_active= True
    )


@pytest.fixture
def category_repository() -> DjangoORMCategoryRepository:
    return DjangoORMCategoryRepository()


@pytest.mark.django_db
class TestListAPI:
    def test_list_categories(
        self,
        category_1: Category,
        category_2: Category,
        category_repository: DjangoORMCategoryRepository,
    ) -> None:
        category_repository.save(category_1)
        category_repository.save(category_2)

        url = "/api/categories/"
        response = APIClient().get(url)

        expected_data = {
            "data": [
                {
                    "id": str(category_1.id),
                    "name": "KITS",
                    "display_name": "KITS",
                    "relationship_id": "",
                    "is_active": True
                }
            ],
            "meta": {
                "current_page": 1,
                "per_page": 10,
                "total": 1,
            },
        }

        assert response.status_code == status.HTTP_200_OK
        response.data['data'][0]['name'] == expected_data['data'][0]['name']

    def test_get_category(
            self,
            category_1: Category,
            category_repository: DjangoORMCategoryRepository,
        ) -> None:
            category_repository.save(category_1)

            url = f"/api/categories/{category_1.id}/"
            response = APIClient().get(url)

            expected_data = {
                "data": 
                    {
                        "id": str(category_1.id),
                        "name": "KITS",
                        "display_name": "KITS",
                        "relationship_id": "",
                        "is_active": True
                    }
            }

            assert response.status_code == status.HTTP_200_OK
            response.data['data']['name'] == expected_data['data']['name']

@pytest.mark.django_db
class TestCreateAPI:
    def test_when_request_data_is_valid_then_return_category(
        self,
        category_repository: DjangoORMCategoryRepository,
    ) -> None:
        url = reverse("category-list")
        data = {
            "name": "KITS",
            "display_name": "KITS",
            "relationship_id": "",
            "is_active": True
        }
        response = APIClient().post(url, data=data)

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["id"]

        saved_category = category_repository.get_by_id(response.data["id"])
        assert saved_category.id == UUID(response.data["id"])

@pytest.mark.django_db
class TestUpdateAPI:
    def test_when_request_data_is_valid_then_update_category(
        self,
        category_1: Category,
        category_repository: DjangoORMCategoryRepository,
    ) -> None:
        category_repository.save(category_1)

        url = reverse("category-detail", kwargs={"pk": category_1.id})
    
        data = {
            "name": "KITS1",
            "display_name": "KITS1",
            "relationship_id": "",
            "is_active": True
        }
        response = APIClient().put(url, data=data)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not response.data
        updated_category = category_repository.get_by_id(category_1.id)
        assert updated_category.name == "KITS1"
        assert updated_category.display_name == "KITS1"
        assert updated_category.relationship_id == ""
        assert updated_category.is_active is True