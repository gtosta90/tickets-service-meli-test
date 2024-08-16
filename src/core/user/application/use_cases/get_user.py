from dataclasses import dataclass
from uuid import UUID
from src.core.user.domain.user_repository import UserRepository
from src.core.user.application.use_cases.exceptions import UserNotFound

from src.core.user.domain.user import User

@dataclass
class GetUserRequest:
    id: int

@dataclass
class GetUserResponse:
    id: int
    name: str
    username: str
    email: str
    
class GetUser:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    def execute(self, request: GetUserRequest) -> GetUserResponse:
        user = self.repository.get_by_id(request.id)

        if user is None:
            raise UserNotFound(f"User with {request.id} not found")

        return GetUserResponse(
            id=user.id,
            name=user.name,
            username=user.username,
            email=user.email,
        )