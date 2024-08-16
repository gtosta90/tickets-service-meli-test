from abc import ABC
from dataclasses import dataclass, field
from typing import Generic, TypeVar
from uuid import UUID

from src.core.user.domain.user_repository import UserRepository

@dataclass
class UserOutput:
    id: UUID
    name: str
    username: str
    email: str

@dataclass
class ListUsersRequest:
    order_by: str = "name"
    current_page: int = 1


@dataclass
class ListOutputMeta:
    current_page: int = 1
    per_page: int = 10
    total: int = 0


T = TypeVar("T")


@dataclass
class ListOutput(Generic[T], ABC):
    data: list[T] = field(default_factory=list)
    meta: ListOutputMeta = field(default_factory=ListOutputMeta)


@dataclass
class ListUsersResponse(ListOutput[UserOutput]):
    pass


class ListUsers:
    def __init__(self, repository: UserRepository) -> None:
        self.repository = repository

    def execute(self, request: ListUsersRequest) -> ListUsersResponse:
        users = self.repository.list()
        ordered_users = sorted(
            users,
            key=lambda user: getattr(user, request.order_by),
        )
        page_offset = (request.current_page - 1) * 2
        users_page = ordered_users[page_offset:page_offset + 2]

        return ListUsersResponse(
            data=sorted(
                [
                    UserOutput(
                        id=user.id,
                        name=user.name,
                        username=user.username,
                        email=user.email
                    ) for user in users_page
                ],
                key=lambda user: getattr(user, request.order_by),
            ),
            meta=ListOutputMeta(
                current_page=request.current_page,
                per_page=10,
                total=len(users),
            ),
        )
