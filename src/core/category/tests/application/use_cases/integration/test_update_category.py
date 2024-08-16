import uuid

from src.core.category.application.use_cases.update_category import (
    UpdateCategory,
    UpdateCategoryRequest,
)
from src.core.category.domain.category import Category
from src.core.category.infra.in_memory_category_repository import (
    InMemoryCategoryRepository,
)


class TestUpdateCategory:
    def test_update_category_with_provided_fields(self):
        category = Category(
            name="KITS",
            display_name="KITS",
            relationship_id = "",
            is_active=True
        )
        repository = InMemoryCategoryRepository()
        repository.save(category=category) 
        use_case = UpdateCategory(repository=repository)

        request = UpdateCategoryRequest(
            id=category.id,
            name="KITS1",
            display_name="KITS1",
            relationship_id = category.id,
            is_active=False,
        )
        response = use_case.execute(request)

        updated_category = repository.get_by_id(category.id)
        assert response is None
        assert updated_category.name == "KITS1"
        assert updated_category.display_name == "KITS1"
        assert updated_category.relationship_id == request.relationship_id
        assert updated_category.is_active is False
