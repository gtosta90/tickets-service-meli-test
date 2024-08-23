import logging
from abc import ABC
from src import config
from dataclasses import dataclass, field
from typing import Generic, TypeVar
from uuid import UUID
from datetime import datetime

from core.category.domain.category import Category
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
    per_page: int = 10

@dataclass
class ListOutputMeta:
    current_page: int = 1
    per_page: int = 10
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
    logger = logging.getLogger('tickets-service')
    def __init__(self, repository: CategoryRepository) -> None:
        self.repository = repository

    def execute(self, request: ListCategoriesRequest) -> ListCategoriesResponse:
        categories = self.repository.list()
        ordered_categories = sorted(
            categories,
            key=lambda category: getattr(category, request.order_by),
        )
        try:
            new_ordered_categories = []
            for category_resp in ordered_categories:
                self._get_subcategories(self.repository ,category_resp)
                new_ordered_categories.append(category_resp)
        except ValueError as err:
            self.logger.error(err)
            raise ValueError

        page_offset = (request.current_page - 1) * request.per_page
        categories_page = new_ordered_categories[page_offset:page_offset + request.per_page]

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
                        subcategories=category.subcategories
                    ) for category in categories_page
                ],
                key=lambda category: getattr(category, request.order_by),
            ),
            meta=ListOutputMeta(
                current_page=request.current_page,
                per_page=request.per_page,
                total=len(categories),
            ),
        )
    
    def _get_subcategories(self, repo: CategoryRepository, category_resp: Category):
        subcategory_list = repo.list_by_relationship_id(category_resp.id)
        category_resp.subcategories = subcategory_list   
        if len(subcategory_list) > 0:
            #itera a lista recursivo
            for subcategory in subcategory_list:
                self._get_subcategories(repo, subcategory)        
        else:
            return category_resp