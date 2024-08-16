from typing import List
import uuid, datetime
from dataclasses import dataclass, field
from uuid import UUID

from src.core._shared.domain.entity import Entity

@dataclass(eq=False)
class Category(Entity):
    name: str
    display_name: str
    relationship_id: str = ""
    created_at: datetime = datetime.datetime.now()
    updated_at: datetime = None
    is_active: bool = True
    subcategories: List = field(default_factory=list)
    
    def __post_init__(self):
        self.validate()

    def validate(self):
        if not self.name:
            # raise ValueError("name cannot be empty")
            self.notification.add_error("name cannot be empty")
        
        if len(self.name) > 100:
            # raise ValueError("name cannot be longer than 100")
            self.notification.add_error("name cannot be longer than 100")

        
        if not self.display_name:
            # raise ValueError("display_name cannot be empty")
            self.notification.add_error("display_name cannot be empty")
        
        if len(self.display_name) > 50:
            # raise ValueError("display_name cannot be longer than 50")
            self.notification.add_error("display_name cannot be longer than 50")

        if self.notification.has_errors:
            raise ValueError(self.notification.messages)

    def __str__(self):
        return f"{self.name} - {self.display_name} - {self.relationship_id} - ({self.is_active})"

    def __repr__(self):
        return f"<Category {self.name} - {self.display_name} - ({self.id})>"

    def update_category(self, name, display_name):
        self.name = name
        self.display_name = display_name
        self.updated_at = datetime.datetime.now()
        
        self.validate()

    def set_relationship(self, relationship_id):
            self.relationship_id = relationship_id

    def activate(self):
        self.is_active = True

        self.validate()

    def deactivate(self):
        self.is_active = False

        self.validate()