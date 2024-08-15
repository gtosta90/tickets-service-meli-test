from dataclasses import dataclass
from typing import Set
from uuid import UUID

from core._shared.domain.notification import Notification
from src.core.category.application.use_cases.exceptions import InvalidCategory, RelatedEntitiesNotFound
from src.core.category.domain.category import Category
from src.core.category.domain.category_repository import CategoryRepository
from src.core.category.application.use_cases.validates import Validates

@dataclass
class CreateCategoryRequest:
    name: str
    display_name: str
    relationship_id: str = ""
    is_active: bool = True

@dataclass
class CreateCategoryResponse:
    id: UUID

class CreateCategory:
    def __init__(self, repository: CategoryRepository):
        self._repository = repository

    def execute(self, request: CreateCategoryRequest) -> CreateCategoryResponse:
        notification = Notification()
        validates = Validates()
        notification.add_errors(validates.validate_relationship_category(category_id=request.relationship_id, category_repository=self._repository))

        if notification.has_errors:
            raise RelatedEntitiesNotFound(notification.messages)
    
        try:
            category = Category(
                name = request.name,
                display_name = request.display_name,
                relationship_id = request.relationship_id,
                is_active = request.is_active
            )
        except ValueError as err:
            raise InvalidCategory(err)

        self._repository.save(category)
        return CreateCategoryResponse(id=category.id)
