from abc import ABC, abstractmethod

from src.core.user.domain.user import User


class UserRepository(ABC):

    @abstractmethod
    def get_by_id(self, id: int) -> User | None:
        raise NotImplementedError

    @abstractmethod
    def list(self) -> list[User]:
        raise NotImplementedError