class Person:
    """Represents a generic base class for individuals in the system."""
    
    def __init__(self, name: str):
        self._name = name

    @property
    def name(self) -> str:
        """Getter for the person's name."""
        return self._name

    @name.setter
    def name(self, value: str):
        """Setter for the person's name with validation."""
        if not value.strip():
            raise ValueError("Name cannot be empty.")
        self._name = value.strip()
