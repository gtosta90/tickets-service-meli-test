from dataclasses import dataclass
from uuid import UUID
from core.category.domain.category_repository import CategoryRepository

@dataclass
class Validates:
    def validate_category(self, category_id: UUID, category_repository: CategoryRepository) -> list[str]:
        if category_id:
            existing_category_id = [{category.id for category in category_repository.list()}]
            if any(category_id not in i for i in existing_category_id):
                return ["Invalid category"]
            return []
        return[]
    
    def validate_relationship_category(self, category_id: UUID, category_repository: CategoryRepository) -> list[str]:
        if category_id:
            existing_category_id = [{category.id for category in category_repository.list()}]
            if any(category_id not in i for i in existing_category_id):
                return ["Invalid category"]
            return []
        return[]