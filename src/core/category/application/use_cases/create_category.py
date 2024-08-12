from dataclasses import dataclass
from uuid import UUID, uuid4

from src.core.category.application.use_cases.exceptions import InvalidCategory
from src.core.category.domain.category import Category
from src.core.category.domain.category_repository import CategoryRepository

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
        self.repository = repository

    def execute(self, request: CreateCategoryRequest) -> CreateCategoryResponse:
        try:
            category = Category(
                name = request.name,
                display_name = request.display_name,
                relationship_id = request.relationship_id,
                is_active = request.is_active
            )
        except ValueError as err:
            raise InvalidCategory(err)

        self.repository.save(category)
        return CreateCategoryResponse(id=category.id)

