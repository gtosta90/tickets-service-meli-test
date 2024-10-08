from dataclasses import dataclass
from uuid import UUID
from core.category.domain.category_repository import CategoryRepository
from core.user.domain.user_repository import UserRepository

@dataclass
class Validates:
    def validate_user(self, user_id: int, user_repository: UserRepository) -> list[str]:
            existing_user_ids = [{user.id for user in user_repository.list()}]
            if any(user_id not in i for i in existing_user_ids):
                return ["Invalid user_created"]
            return []

    def validate_user_assigned(self, user_id: int, user_repository: UserRepository) -> list[str]:
        if user_id > 0:
            existing_user_ids = user_repository.get_by_id(id=user_id)
            if not existing_user_ids:
                return ["Invalid user_assigned"]
            return []
        return[]

    def validate_category(self, category_id: UUID, category_repository: CategoryRepository) -> list[str]:
        if category_id:
            existing_category_id = category_repository.get_by_id(id=category_id)
            if not existing_category_id:
                return ["Invalid category"]
            return []
    
    def validate_subcategory(self, category_id: UUID, subcategory_id: UUID, category_repository: CategoryRepository) -> list[str]:
        if subcategory_id:
            existing_subcategory = category_repository.get_by_id(id=subcategory_id)
            if not existing_subcategory:
                return ["Invalid subcategory"]
            else:
                # import ipdb; ipdb.set_trace()
                if str(existing_subcategory.relationship_id) != str(category_id):
                    return ["The subcategory id is not a subcategory of the main category submitted"]
                return []