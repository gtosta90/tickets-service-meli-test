import pytest
from uuid import UUID
import uuid

from src.core.category.domain.category import Category


class TestCategory:
    def test_name_is_required(self):
        with pytest.raises(
            TypeError, match="missing 1 required positional argument: 'name'"
        ):
            Category(display_name="a")

    def test_name_must_have_less_than_100_characters(self):
        with pytest.raises(ValueError, match="name cannot be longer than 100"):
            Category(name="a" * 101, display_name="a")

    def test_display_name_is_required(self):
        with pytest.raises(
            TypeError, match="missing 1 required positional argument: 'display_name'"
        ):
            Category(name="a")

    def test_name_must_have_less_than_50_characters(self):
        with pytest.raises(ValueError, match="name cannot be longer than 50"):
            Category(name="a", display_name="a" * 51)

    def test_category_must_be_created_with_id_as_uuid_by_default(self):
        category = Category(name="KITS", display_name="KITS")
        assert isinstance(category.id, UUID)

    def test_create_category_with_default_values(self):
        category = Category(name="KITS", display_name="KITS")
        assert category.name == "KITS"
        assert category.display_name == "KITS"
        assert category.created_at is not None
        assert category.is_active is True

    def test_create_category_as_active_by_default(self):
        category = Category(name="KITS", display_name="KITS")
        assert category.is_active is True

    def test_create_category_with_provided_values(self):
        category_id = uuid.uuid4()
        category = Category(
            id=category_id,
            name="KITS",
            display_name="KITS",
            is_active=False,
        )

        assert category.id == category_id
        assert category.name == "KITS"
        assert category.display_name == "KITS"
        assert category.is_active is False

    def test_cannot_create_category_with_empty_name(self):
        with pytest.raises(ValueError, match="name cannot be empty"):
            Category(name="", display_name="KITS")

    def test_cannot_create_category_with_display_name_longer_than_50(self):
        with pytest.raises(ValueError, match="display_name cannot be longer than 50"):
            Category(name="KITS", display_name="a" * 51)

class TestUpdateCategory:
    def test_update_category_with_name_and_display_name(self):
        category = Category(
            name="KITS", 
            display_name="KITS",
        )

        category.update_category(
            name="KITS1", 
            display_name="KITS1",
        )

        assert category.name == "KITS1"
        assert category.display_name == "KITS1"


    def test_update_category_with_invalid_name_raises_exception(self):
        category = Category(name="KITS", display_name="KITS")

        with pytest.raises(ValueError, match="name cannot be longer than 100"):
            category.update_category(name="a" * 101, display_name="KITS")

    def test_cannot_update_category_with_empty_name(self):
        category = Category(name="KITS", display_name="KITS")

        with pytest.raises(ValueError, match="name cannot be empty"):
            category.update_category(name="", display_name="Qualquer nome")

    def test_update_category_with_invalid_display_name_raises_exception(self):
        category = Category(name="KITS", display_name="KITS")

        with pytest.raises(ValueError, match="display_name cannot be longer than 50"):
            category.update_category(name="KITS1", display_name="KITS1" * 51)

    def test_cannot_update_category_with_empty_display_name(self):
        category = Category(name="KITS", display_name="KITS")

        with pytest.raises(ValueError, match="name cannot be empty"):
            category.update_category(name="KITS1", display_name="")


class TestSetRelationship:
    def test_set_realtionship_when_category_relationship_empty(self):
        category = Category(
            name="KITS",
            display_name="KITS",
            is_active=False,
        )

        category.set_relationship(uuid.uuid4())

        assert category.relationship_id is not None

    # def test_set_realtionship_when_category_relationship_not_empty(self):
    #     category = Category(
    #         name="KITS",
    #         display_name="KITS",
    #         relationship_id=uuid.uuid4(),
    #         is_active=True,
    #     )
    #     with pytest.raises(ValueError, match="relationship_id cannot be updated"):
    #         category.set_relationship(uuid.uuid4())

class TestActivate:
    def test_activate_inactive_category(self):
        category = Category(
            name="KITS",
            display_name="KITS",
            is_active=False,
        )

        category.activate()

        assert category.is_active is True

    def test_activate_active_category(self):
        category = Category(
            name="KITS",
            display_name="KITS",
            is_active=True,
        )

        category.activate()

        assert category.is_active is True


class TestDeactivate:
    def test_deactivate_active_category(self):
        category = Category(
            name="KITS",
            display_name="KITS",
            is_active=True,
        )

        category.deactivate()

        assert category.is_active is False

    def test_deactivate_inactive_category(self):
        category = Category(
            name="KITS",
            display_name="KITS",
            is_active=False,
        )

        category.deactivate()

        assert category.is_active is False


class TestEquality:
    def test_when_categorys_have_same_id_they_are_equal(self):
        common_id = uuid.uuid4()
        category_1 = Category(name="KITS", display_name="KITS", id=common_id)
        category_2 = Category(name="KITS1", display_name="KITS1", id=common_id)

        assert category_1 == category_2

    def test_equality_different_classes(self):
        class Dummy:
            pass

        common_id = uuid.uuid4()
        category = Category(name="KITS", display_name="KITS", id=common_id)
        dummy = Dummy()
        dummy.id = common_id

        assert category != dummy
