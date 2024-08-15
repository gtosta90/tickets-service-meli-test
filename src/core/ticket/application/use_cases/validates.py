from dataclasses import dataclass
from uuid import UUID
from core.category.domain.category_repository import CategoryRepository
from core.user.domain.user_repository import UserRepository

@dataclass
class Validates:
    def validate_user(self, user_id: int, user_repository: UserRepository) -> list[str]:
            existing_user_ids = [{user.id for user in user_repository.list()}]
            if any(user_id not in i for i in existing_user_ids):
                return ["Invalid User"]
            return []

    def validate_user_assigned(self, user_id: int, user_repository: UserRepository) -> list[str]:
        if user_id > 0:
            existing_user_ids = [{user.id for user in user_repository.list()}]
            if any(user_id not in i for i in existing_user_ids):
                return ["Invalid User"]
            return []
        return[]

    def validate_category(self, category_id: UUID, category_repository: CategoryRepository) -> list[str]:
        if category_id:
            existing_category_id = [{category.id for category in category_repository.list()}]
            if any(category_id not in i for i in existing_category_id):
                return ["Invalid category"]
            return []
        return[]