from unittest.mock import create_autospec
import uuid

import pytest
from src.core.category.domain.category_repository import CategoryRepository
from src.core.category.application.use_cases.exceptions import CategoryNotFound, InvalidCategory
from src.core.category.application.use_cases.update_category import UpdateCategory, UpdateCategoryRequest
from src.core.category.domain.category import Category


class TestUpdateCategory:
    @pytest.fixture
    def category(self) -> Category:
        return Category(
            name="KITS",
            display_name="KITS"
        )

    @pytest.fixture
    def mock_repository(self, category: Category) -> CategoryRepository:
        repository = create_autospec(CategoryRepository, instance=True)
        repository.get_by_id.return_value = category
        return repository

    def test_update_category_name_and_display_name(
        self,
        mock_repository: CategoryRepository,
        category: Category,
    ):
        use_case = UpdateCategory(mock_repository)
        use_case.execute(UpdateCategoryRequest(
            id=category.id,
            name=category.name,
            display_name=category.display_name,
        ))

        assert category.name == "KITS"
        assert category.display_name == "KITS"
        mock_repository.update.assert_called_once_with(category)

    def test_update_category_relationship(
        self,
        mock_repository: CategoryRepository,
        category: Category,
    ):
        use_case = UpdateCategory(mock_repository)
        relationship_id = uuid.uuid4()
        use_case.execute(UpdateCategoryRequest(
            id=category.id,
            relationship_id=relationship_id
        ))

        assert category.relationship_id == relationship_id
        mock_repository.update.assert_called_once_with(category)

    def test_activate_category(
        self,
        mock_repository: CategoryRepository,
        category: Category,
    ) -> None:
        category.deactivate()

        use_case = UpdateCategory(mock_repository)
        use_case.execute(UpdateCategoryRequest(
            id=category.id,
            name="KITS",
            is_active=True,
        ))

        assert category.is_active is True
        mock_repository.update.assert_called_once_with(category)

    def test_deactivate_category(
        self,
        mock_repository: CategoryRepository,
        category: Category,
    ) -> None:
        category.activate()

        use_case = UpdateCategory(mock_repository)
        use_case.execute(UpdateCategoryRequest(
            id=category.id,
            is_active=False,
        ))

        assert category.is_active is False
        mock_repository.update.assert_called_once_with(category)

    def test_when_category_is_updated_to_invalid_state_then_raise_exception(
        self,
        mock_repository: CategoryRepository,
        category: Category,
    ) -> None:
        use_case = UpdateCategory(mock_repository)
        request = UpdateCategoryRequest(
            id=category.id,
            name="",
        )

        with pytest.raises(InvalidCategory) as exc:
            use_case.execute(request)

        mock_repository.update.assert_not_called()
        assert str(exc.value) == "name cannot be empty"
