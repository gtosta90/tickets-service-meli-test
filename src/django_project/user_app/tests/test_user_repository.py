import uuid
import pytest
from django_project.user_app.repository import ApiClientUserRepository
from src.core.user.domain.user import User


class TestSave:
    def test_list_users_in_users_api(self):
        repository = ApiClientUserRepository()

        users = repository.list()

        assert len(users) >= 9

    def test_get_user_by_id_users_api(self):
        repository = ApiClientUserRepository()

        user = repository.get_by_id(1)

        assert user.id == 1
        assert user.name == "Leanne Graham"
        assert user.username == "Bret"
        assert user.email == "Sincere@april.biz"