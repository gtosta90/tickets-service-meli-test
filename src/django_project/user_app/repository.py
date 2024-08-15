from typing import List
from uuid import UUID, uuid4
from apiclient import APIClient
import json
from core.user.domain.user_repository import UserRepository
from core.user.domain.user import User

class ApiClientUserRepository(UserRepository):
    def __init__(self, domain: User | None = None):
        self.domain = domain or User

    def get_by_id(self, id: int) -> User | None:
        try:
            url = f"https://jsonplaceholder.typicode.com/users/{id}"
            resp = APIClient().get(url)
            return UserDomainMapper.to_entity(json.loads(resp.content))
        except Exception:
            return None

    def list(self) -> list[User]:
        url = "https://jsonplaceholder.typicode.com/users/"
        resp = APIClient().get(url)
        return [UserDomainMapper.to_entity(user) for user in json.loads(resp.content)]

class UserDomainMapper:
    @staticmethod
    def to_entity(json: json) -> User:
        return User(
            id=json["id"],
            name=json["name"],
            username=json["username"],
            email=json["email"]
        )