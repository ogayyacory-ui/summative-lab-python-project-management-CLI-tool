class Person:
    """Base class representing a general individual."""
    def __init__(self, name: str):
        self._name = name

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str):
        if not value.strip():
            raise ValueError("Name cannot be empty.")
        self._name = value


class User(Person):
    """User class inheriting from Person, adding email and project tracking."""
    def __init__(self, name: str, email: str):
        super().__init__(name)
        self.email = email

    @property
    def email(self) -> str:
        return self._email

    @email.setter
    def email(self, value: str):
        if "@" not in value or "." not in value:
            raise ValueError("Invalid email format.")
        self._email = value

    def to_dict(self) -> dict:
        """Serializes the User object to a dictionary."""
        return {"name": self.name, "email": self.email}

    @classmethod
    def from_dict(cls, data: dict):
        """Creates a User instance from a dictionary."""
        return cls(name=data["name"], email=data["email"])

    def __repr__(self) -> str:
        return f"<User: {self.name} ({self.email})>"