from dataclasses import dataclass, field

@dataclass
class User():
    id: int
    name: str
    username: str
    email: str
    
    def __post_init__(self):
        self.validate()

    def validate(self):
        if not self.name:
            raise ValueError("title cannot be empty")
        
        if len(self.name) > 255:
            raise ValueError("title cannot be longer than 255")
        
        if not self.username:
            raise ValueError("user_create cannot be empty")
        
        if not self.email:
            raise ValueError("category cannot be empty")

    def __str__(self):
        return f"{self.name} - {self.username} - {self.email}"

    def __repr__(self):
        return f"<User {self.name} - {self.username} - ({self.email})>"

    def __eq__(self, other):
        if not isinstance(other, User):
            return False

        return self.id == other.id