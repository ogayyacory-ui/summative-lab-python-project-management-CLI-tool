from models.person import Person

class User(Person):
    """Represents a system User inheriting from Person (Demonstrating Inheritance)."""
    
    def __init__(self, name: str, email: str):
        super().__init__(name)
        self.email = email  # Triggers property setter validation

    @property
    def email(self) -> str:
        """Getter for user email."""
        return self._email

    @email.setter
    def email(self, value: str):
        """Setter for user email validating basic syntax."""
        if "@" not in value or "." not in value:
            raise ValueError(f"Invalid email address format: {value}")
        self._email = value.strip()

    def to_dict(self) -> dict:
        """Serializes the object to a dictionary for JSON conversion."""
        return {"name": self.name, "email": self.email}

    @classmethod
    def from_dict(cls, data: dict):
        """Factory method to construct a User object from parsed JSON data."""
        return cls(name=data["name"], email=data["email"])

    def __repr__(self) -> str:
        return f"<User name='{self.name}', email='{self.email}'>"