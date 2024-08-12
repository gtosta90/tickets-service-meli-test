from dataclasses import dataclass
from datetime import datetime
from uuid import UUID
from src.core.category.domain.category_repository import CategoryRepository
from src.core.category.application.use_cases.exceptions import CategoryNotFound

from src.core.category.domain.category import Category

@dataclass
class GetCategoryRequest:
    id: UUID

@dataclass
class GetCategoryResponse:
    id: UUID
    name: str
    display_name: str
    relationship_id: str
    created_at: datetime
    updated_at: datetime
    is_active: bool
    subcategories: list


class GetCategory:
    def __init__(self, repository: CategoryRepository):
        self.repository = repository

    def execute(self, request: GetCategoryRequest) -> GetCategoryResponse:
        category = self.repository.get_by_id(request.id)

        if category is None:
            raise CategoryNotFound(f"Category with {request.id} not found")

        return GetCategoryResponse(
            id=category.id,
            name=category.name,
            display_name=category.display_name,
            relationship_id=category.relationship_id,
            created_at=category.created_at,
            updated_at=category.updated_at,
            is_active=category.is_active,
            subcategories=[]
        )