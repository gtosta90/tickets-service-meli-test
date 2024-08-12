from unittest.mock import create_autospec

import pytest
from src.core.category.application.use_cases.list_categories import (
    CategoryOutput,
    ListCategories,
    ListCategoriesRequest,
    ListCategoriesResponse, ListOutputMeta,
)
from src.core.category.domain.category import Category
from src.core.category.domain.category_repository import CategoryRepository


class TestListCategories:
    @pytest.fixture
    def category_1(self) -> Category:
        return Category(
            name="KITS",
            display_name="KITS",
        )

    @pytest.fixture
    def category_2(self) -> Category:
        return Category(
            name="KITS1",
            display_name="KITS1",
        )

    @pytest.fixture
    def category_3(self) -> Category:
        return Category(
            name="KITS2",
            display_name="KITS2",
        )

    @pytest.fixture
    def mock_empty_repository(self) -> CategoryRepository:
        repository = create_autospec(CategoryRepository)
        repository.list.return_value = []
        return repository

    @pytest.fixture
    def mock_populated_repository(
        self,
        category_1: Category,
        category_2: Category,
        category_3: Category,
    ) -> CategoryRepository:
        repository = create_autospec(CategoryRepository)
        repository.list.return_value = [
            category_1,
            category_2,
            category_3
        ]
        return repository

    def test_when_no_categories_then_return_empty_list(
        self,
        mock_empty_repository: CategoryRepository,
    ) -> None:
        use_case = ListCategories(repository=mock_empty_repository)
        response = use_case.execute(request=ListCategoriesRequest())

        assert response == ListCategoriesResponse(
            data=[],
            meta=ListOutputMeta(
                current_page=1,
                per_page=2,
                total=0,
            ),
        )

    def test_when_category_exist_then_return_mapped_list(
        self,
        mock_populated_repository: CategoryRepository,
        category_1: Category,
        category_2: Category,
        category_3: Category,
    ) -> None:
        use_case = ListCategories(repository=mock_populated_repository)
        response = use_case.execute(request=ListCategoriesRequest())

        print(response)

        assert response == ListCategoriesResponse(
            data=[
                CategoryOutput(
                    id=category_1.id,
                    name=category_1.name,
                    display_name=category_1.display_name,
                    relationship_id=category_1.relationship_id,
                    created_at=category_1.created_at,
                    updated_at=category_1.updated_at,
                    is_active=category_1.is_active,
                    subcategories=[]
                ),
                CategoryOutput(
                    id=category_2.id,
                    name=category_2.name,
                    display_name=category_2.display_name,
                    relationship_id=category_2.relationship_id,
                    created_at=category_2.created_at,
                    updated_at=category_2.updated_at,
                    is_active=category_2.is_active,
                    subcategories=[]
                )
                # link_air vem antes, "empurra" o link_used para fora da página
            ],
            meta=ListOutputMeta(
                current_page=1,
                per_page=2,
                total=3,
            ),
        )

    def test_fetch_page_without_elements(self, mock_populated_repository: CategoryRepository) -> None:
        use_case = ListCategories(repository=mock_populated_repository)
        response = use_case.execute(request=ListCategoriesRequest(current_page=3))

        assert response == ListCategoriesResponse(
            data=[],
            meta=ListOutputMeta(
                current_page=3,
                per_page=2,
                total=3,
            ),
        )

    def test_fetch_last_page_with_elements(
        self,
        mock_populated_repository: CategoryRepository,
        category_3: Category,  # Foi "empurrado" para última página
    ) -> None:
        use_case = ListCategories(repository=mock_populated_repository)
        response = use_case.execute(request=ListCategoriesRequest(current_page=2))

        assert response == ListCategoriesResponse(
            data=[
                CategoryOutput(
                    id=category_3.id,
                    name=category_3.name,
                    display_name=category_3.display_name,
                    relationship_id=category_3.relationship_id,
                    created_at=category_3.created_at,
                    updated_at=category_3.updated_at,
                    is_active=category_3.is_active,
                    subcategories=[]
                )
            ],
            meta=ListOutputMeta(
                current_page=2,
                per_page=2,
                total=3,
            ),
        )
