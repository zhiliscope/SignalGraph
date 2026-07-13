class Entity:
    """A node in the knowledge graph."""

    def __init__(self, entity_id: str, entity_type: str, name: str) -> None:
        self.id = entity_id
        self.type = entity_type
        self.name = name

    def __repr__(self) -> str:
        return (
            f"Entity(id={self.id!r}, type={self.type!r}, "
            f"name={self.name!r})"
        )
