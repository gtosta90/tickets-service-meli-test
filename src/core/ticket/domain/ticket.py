import uuid, datetime
from dataclasses import dataclass, field
from uuid import UUID
from core._shared.domain.entity import Entity
from src.core.ticket.domain.value_objects import Status, Level

@dataclass(eq=False)
class Ticket(Entity):
    title: str
    user_create: int
    category: UUID
    severity: Level
    description: str = ""
    created_at: datetime = datetime.datetime.now()
    updated_at: datetime = None
    user_assigned: int = 0
    status: Status = Status.OPEN
    
    def __post_init__(self):
        self.validate()

    def validate(self):
        if not self.title:
            # raise ValueError("title cannot be empty")
            self.notification.add_error("title cannot be empty")

        if len(self.title) > 255:
            # raise ValueError("title cannot be longer than 255")
            self.notification.add_error("title cannot be longer than 255")
        
        if not self.user_create:
            # raise ValueError("user_create cannot be empty")
            self.notification.add_error("user_create cannot be empty")
        
        if not self.category:
            # raise ValueError("category cannot be empty")
            self.notification.add_error("category cannot be empty")
        
        if not self.severity:
            # raise ValueError("severity cannot be empty")
            self.notification.add_error("severity cannot be empty")
        
        if len(self.description) > 1024:
            # raise ValueError("description cannot be longer than 1024")
            self.notification.add_error("description cannot be longer than 1024")

        if self.notification.has_errors:
            raise ValueError(self.notification.messages)
        
    def __str__(self):
        return f"{self.title} - {self.user_create} - {self.category} - {self.severity} - {self.status} ({self.is_active})"

    def __repr__(self):
        return f"<Category {self.title} - {self.user_create} - ({self.id})>"

    def update_ticket(self, title, category, severity, description, user_assigned, status):
        self.title = title
        self.category = category
        self.severity = severity
        self.description = description
        self.user_assigned = user_assigned
        self.status = status
        self.updated_at = datetime.datetime.now()

        self.validate()
