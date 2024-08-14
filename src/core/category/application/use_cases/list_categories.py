from abc import ABC
from dataclasses import dataclass, field
from typing import Generic, TypeVar
from uuid import UUID
from datetime import datetime

from src.core.category.domain.category_repository import CategoryRepository

@dataclass
class CategoryOutput:
    id: UUID
    name: str
    display_name: str
    relationship_id: str
    created_at: datetime
    updated_at: datetime
    is_active: bool
    subcategories: list = None


@dataclass
class ListCategoriesRequest:
    order_by: str = "name"
    current_page: int = 1


@dataclass
class ListOutputMeta:
    current_page: int = 1
    per_page: int = 2
    total: int = 0


T = TypeVar("T")


@dataclass
class ListOutput(Generic[T], ABC):
    data: list[T] = field(default_factory=list)
    meta: ListOutputMeta = field(default_factory=ListOutputMeta)


@dataclass
class ListCategoriesResponse(ListOutput[CategoryOutput]):
    pass


class ListCategories:
    def __init__(self, repository: CategoryRepository) -> None:
        self.repository = repository

    def execute(self, request: ListCategoriesRequest) -> ListCategoriesResponse:
        categories = self.repository.list()
        ordered_categories = sorted(
            categories,
            key=lambda category: getattr(category, request.order_by),
        )
        page_offset = (request.current_page - 1) * 2
        categories_page = ordered_categories[page_offset:page_offset + 2]

        return ListCategoriesResponse(
            data=sorted(
                [
                    CategoryOutput(
                        id=category.id,
                        name=category.name,
                        display_name=category.display_name,
                        relationship_id=category.relationship_id,
                        created_at=category.created_at,
                        updated_at=category.updated_at,
                        is_active=category.is_active,
                        subcategories=[]
                    ) for category in categories_page
                ],
                key=lambda category: getattr(category, request.order_by),
            ),
            meta=ListOutputMeta(
                current_page=request.current_page,
                per_page=2,
                total=len(categories),
            ),
        )
