from dataclasses import dataclass, field
from datetime import datetime
from typing import List
from uuid import UUID
from src.core.category.domain.category import Category
from src.core.category.domain.category_repository import CategoryRepository
from src.core.category.application.use_cases.exceptions import CategoryNotFound

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
    subcategories: List = field(default_factory=list)



class GetCategory:
    def __init__(self, repository: CategoryRepository):
        self.repository = repository

    def execute(self, request: GetCategoryRequest) -> GetCategoryResponse:
        category = self.repository.get_by_id(request.id)

        if category is None:
            raise CategoryNotFound(f"Category with {request.id} not found")

        category_response = GetCategoryResponse(
            id=category.id,
            name=category.name,
            display_name=category.display_name,
            relationship_id=category.relationship_id,
            created_at=category.created_at,
            updated_at=category.updated_at,
            is_active=category.is_active
        )

        _get_subcategories(self.repository, category_response)

        return category_response 
    
def _get_subcategories(repo: CategoryRepository, category_resp: GetCategoryResponse):
    subcategory_list = repo.list_by_relationship_id(category_resp.id)
    category_resp.subcategories = subcategory_list

    if len(subcategory_list) > 0:
        #itera a lista recursivo
        for subcategory in subcategory_list:
            _get_subcategories(repo, subcategory)
    else:
        return category_resp