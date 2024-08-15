import pytest

from src.core.category.application.use_cases.list_categories import (
    CategoryOutput,
    ListCategories,
    ListCategoriesRequest,
    ListCategoriesResponse, ListOutputMeta,
)
from src.core.category.domain.category import Category
from src.core.category.infra.in_memory_category_repository import (
    InMemoryCategoryRepository,
)


class TestListCategory:
    @pytest.fixture
    def category_1(self) -> Category:
        return Category(
            name="KITS",
            display_name="KITS",
            relationship_id = "",
            is_active=True
        )

    @pytest.fixture
    def category_2(self) -> Category:
        return Category(
            name="KITS1",
            display_name="KITS1",
            relationship_id = "",
            is_active=True
        )

    @pytest.fixture
    def category_3(self) -> Category:
        return Category(
            name="KITS2",
            display_name="KITS2",
            relationship_id = "",
            is_active=True
        )

    def test_when_no_categories_then_return_empty_list(self) -> None:
        empty_repository = InMemoryCategoryRepository()
        use_case = ListCategories(repository=empty_repository)
        response = use_case.execute(request=ListCategoriesRequest())

        assert response == ListCategoriesResponse(
            data=[],
            meta=ListOutputMeta(),
        )

    def test_when_categories_exist_then_return_mapped_list(
        self,
        category_1: Category,
        category_2: Category,
        category_3: Category,
    ) -> None:
        repository = InMemoryCategoryRepository()
        repository.save(category=category_1)
        repository.save(category=category_2)
        repository.save(category=category_3)

        use_case = ListCategories(repository=repository)
        response = use_case.execute(request=ListCategoriesRequest())

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
                ),
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
                current_page=1,
                per_page=10,
                total=3,
            ),
        )
