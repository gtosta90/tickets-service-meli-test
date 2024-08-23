from typing import List
from uuid import UUID, uuid4
from core.category.domain.category_repository import CategoryRepository
from core.category.domain.category import Category
from django_project.category_app.models import Category as CategoryORM


class DjangoORMCategoryRepository(CategoryRepository):
    def __init__(self, model: CategoryORM | None = None):
        self.model = model or CategoryORM

    def save(self, category: Category) -> None:
        category_model = CategoryModelMapper.to_model(category)
        category_model.save()

    def get_by_id(self, id: UUID) -> Category | None:
        try:
            category_model = self.model.objects.get(id=id)
            return CategoryModelMapper.to_entity(category_model)
        except self.model.DoesNotExist:
            return {}
    
    def list_by_relationship_id(self, id: UUID) -> List[Category]:
        return [CategoryModelMapper.to_entity(category) for category in self.model.objects.all().filter(relationship_id=id)]
        
    def delete(self, id: UUID) -> None:
        self.model.objects.filter(pk=id).delete()
        # self.model.objects.filter(pk=id).update(
        #     is_active=False,
        # )
        #self.model.objects.filter(id=id).delete()

    def list(self) -> list[Category]:
        return [CategoryModelMapper.to_entity(category) for category in self.model.objects.all().filter(relationship_id="")]

    def update(self, category: Category) -> None:
        self.model.objects.filter(pk=category.id).update(
            name=category.name,
            display_name=category.display_name,
            relationship_id=category.relationship_id,
            is_active=category.is_active,
            updated_at=category.updated_at
        )


class CategoryModelMapper:
    @staticmethod
    def to_entity(model: CategoryORM) -> Category:
        return Category(
            id=model.id,
            name=model.name,
            display_name=model.display_name,
            relationship_id=model.relationship_id,
            created_at=model.created_at,
            updated_at=model.updated_at,
            is_active=model.is_active
        )

    @staticmethod
    def to_model(entity: Category) -> CategoryORM:
        return CategoryORM(
            id=entity.id,
            name=entity.name,
            display_name=entity.display_name,
            relationship_id=entity.relationship_id,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
            is_active=entity.is_active
        )
