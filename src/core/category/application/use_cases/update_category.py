
from dataclasses import dataclass
from typing import Set
from uuid import UUID
from core._shared.domain.notification import Notification
from core.category.application.use_cases.validates import Validates
from src.core.category.domain.category_repository import CategoryRepository
from src.core.category.application.use_cases.exceptions import CategoryNotFound, InvalidCategory, RelatedEntitiesNotFound

@dataclass
class UpdateCategoryRequest:
    id: UUID
    name: str | None = None
    display_name: str | None = None
    relationship_id: str | None = None
    is_active: bool | None = None

class UpdateCategory:
    def __init__(self, repository: CategoryRepository):
        self._repository = repository

    def execute(self, request: UpdateCategoryRequest) -> None:
        notification = Notification()        
        validates = Validates()
        notification.add_errors(validates.validate_relationship_category(category_id=request.id, relationship_id=request.relationship_id, category_repository=self._repository))

        if notification.has_errors:
            raise RelatedEntitiesNotFound(notification.messages)
        
        category = self._repository.get_by_id(request.id)
        if category is None:
            raise CategoryNotFound(f"Category with {request.id} not found")

        try:
            if request.is_active is True:
                category.activate()

            if request.is_active is False:
                category.deactivate()

            if request.relationship_id:
                category.set_relationship(request.relationship_id)

            current_name = category.name
            current_display_name = category.display_name

            if request.name is not None:
                current_name = request.name

            if request.display_name is not None:
                current_display_name = request.display_name

            category.update_category(name=current_name, display_name=current_display_name)
        
        except ValueError as error:
            raise InvalidCategory(error)
        # import ipdb; ipdb.set_trace()
        self._repository.update(category)