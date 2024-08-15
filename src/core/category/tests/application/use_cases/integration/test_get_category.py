import uuid

import pytest
from src.core.category.application.use_cases.exceptions import CategoryNotFound
from src.core.category.domain.category import Category
from src.core.category.infra.in_memory_category_repository import InMemoryCategoryRepository
from src.core.category.application.use_cases.get_category import GetCategory, GetCategoryRequest, GetCategoryResponse


class TestGetCategory:
    def test_get_category(self):
        category_1 = Category(
            id=uuid.uuid4(),
            name="KITS",
            display_name="KITS",
            relationship_id = "",
            is_active=True
        )
        category_2 = Category(
            id=uuid.uuid4(),
            name="KITS1",
            display_name="KITS1",
            relationship_id = "",
            is_active=True
        )
        repository = InMemoryCategoryRepository(
            categories=[
                category_1,
                category_2,
            ]
        )

        use_case = GetCategory(repository=repository)
        request = GetCategoryRequest(id=category_1.id)
        response = use_case.execute(request)

        assert response == GetCategoryResponse(
            id=category_1.id,
            name="KITS",
            display_name="KITS",
            relationship_id = "",
            created_at=category_1.created_at,
            updated_at=category_1.updated_at,
            is_active=True,
            subcategories=[]
        )

    def test_when_category_with_id_does_not_exist_then_raise_not_found(self):
        category_1 = Category(
            id=uuid.uuid4(),
            name="KITS",
            display_name="KITS",
            relationship_id = "",
            is_active=True
        )
        category_2 = Category(
            id=uuid.uuid4(),
            name="KITS1",
            display_name="KITS1",
            relationship_id = "",
            is_active=True
        )
        repository = InMemoryCategoryRepository(
            categories=[
                category_1,
                category_2,
            ]
        )

        use_case = GetCategory(repository=repository)
        request = GetCategoryRequest(id="non-existent-id")

        with pytest.raises(CategoryNotFound) as exc:
            use_case.execute(request)

    def test_get_category_with_several_subcategories(self):
        
        category_1 = Category(
            id=uuid.uuid4(),
            name="KITS",
            display_name="KITS",
            relationship_id = "",
            is_active=True
        )

        category_2 = Category(
            id=uuid.uuid4(),
            name="Database",
            display_name="KITS - Database",
            relationship_id=category_1.id,
            is_active=True
        )

        category_3 = Category(
            id=uuid.uuid4(),
            name="Database",
            display_name="KITS - Database - Hija 1",
            relationship_id=category_2.id,
            is_active=True
        )

        category_4 = Category(
            id=uuid.uuid4(),
            name="Oracle",
            display_name="KITS - Database - Oracle",
            relationship_id=category_2.id,
            is_active=True
        )

        category_5 = Category(
            id=uuid.uuid4(),
            name="Database",
            display_name="KITS - BigQueue",
            relationship_id=category_1.id,
            is_active=True
        )
        
        category_6 = Category(
            id=uuid.uuid4(),
            name="Hija 1",
            display_name="KITS - BigQueue - Hija 1",
            relationship_id=category_5.id,
            is_active=True
        )

        category_7 = Category(
            id=uuid.uuid4(),
            name="Database",
            display_name="KITS - BigQueue - Consumer",
            relationship_id=category_5.id,
            is_active=True
        )

        category_8 = Category(
            id=uuid.uuid4(),
            name="Database",
            display_name="KITS - BigQueue - Topic",
            relationship_id=category_5.id,
            is_active=True
        )


        repository = InMemoryCategoryRepository(
            categories=[
                category_1,
                category_2,
                category_3,
                category_4,
                category_5,
                category_6,
                category_7,
                category_8,
            ]
        )

        use_case = GetCategory(repository=repository)
        request = GetCategoryRequest(id=category_1.id)
        response = use_case.execute(request)

        assert len(response.subcategories) == 2
        assert len(response.subcategories[0].subcategories) == 2
        assert len(response.subcategories[1].subcategories) == 3 