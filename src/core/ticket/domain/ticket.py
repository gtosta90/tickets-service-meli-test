import uuid, datetime
from dataclasses import dataclass, field
from uuid import UUID
from core.ticket.domain.value_objects import Status, Level

@dataclass
class Ticket():
    title: str
    user_create: UUID
    category: UUID
    severity: Level
    description: str = ""
    created_at = datetime.datetime.now()
    updated_at = None
    user_assigned: UUID = None
    status: Status = Status.OPEN
    id: UUID = field(default_factory=uuid.uuid4)
    
    def __post_init__(self):
        self.validate()

    def validate(self):
        if not self.title:
            raise ValueError("title cannot be empty")
        
        if len(self.title) > 255:
            raise ValueError("title cannot be longer than 255")
        
        if not self.user_create:
            raise ValueError("user_create cannot be empty")
        
        if not self.category:
            raise ValueError("category cannot be empty")
        
        if not self.severity:
            raise ValueError("severity cannot be empty")
        
        if len(self.description) > 1024:
            raise ValueError("description cannot be longer than 1024")

    def __str__(self):
        return f"{self.title} - {self.user_create} - {self.category} - {self.severity} - {self.status} ({self.is_active})"

    def __repr__(self):
        return f"<Category {self.title} - {self.user_create} - ({self.id})>"

    def __eq__(self, other):
        if not isinstance(other, Ticket):
            return False

        return self.id == other.id

    def update_ticket(self, title, category, severity, description, user_assigned, status):
        self.title = title
        self.category = category
        self.severity = severity
        self.description = description
        self.user_assigned = user_assigned
        self.status = status
        self.updated_at = datetime.datetime.now()

        self.validate()

    def activate(self):
        self.is_active = True

        self.validate()

    def deactivate(self):
        self.is_active = False

        self.validate()
