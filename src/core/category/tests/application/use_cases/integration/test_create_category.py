from uuid import UUID
from src.core.category.application.use_cases.create_category import CreateCategory, CreateCategoryRequest
from src.core.category.infra.in_memory_category_repository import InMemoryCategoryRepository


class TestCreateCategory:
    def test_create_category_with_valid_data(self):
        repository = InMemoryCategoryRepository()
        use_case = CreateCategory(repository=repository)
        request = CreateCategoryRequest(
            name="KITS",
            display_name="KITS",
            relationship_id="",
            is_active = True
        )

        response = use_case.execute(request)

        assert response is not None
        assert isinstance(response.id, UUID)
        assert len(repository.categories) == 1

        persisted_category = repository.categories[0]
        assert persisted_category.id == response.id
        assert persisted_category.name == "KITS"
        assert persisted_category.display_name == "KITS"
        assert persisted_category.relationship_id == ""
        assert persisted_category.is_active == True

    def test_create_inactive_category_with_valid_data(self):
        repository = InMemoryCategoryRepository()
        use_case = CreateCategory(repository=repository)
        request = CreateCategoryRequest(
            name="KITS",
            display_name="KITS",
            relationship_id="",
            is_active = False
        )

        response = use_case.execute(request)
        persisted_category = repository.categories[0]

        assert persisted_category.id == response.id
        assert persisted_category.name == "KITS"
        assert persisted_category.display_name == "KITS"
        assert persisted_category.relationship_id == ""
        assert persisted_category.is_active == False
