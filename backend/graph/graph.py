from collections import Counter, deque
from typing import Optional

from .entity import Entity
from .relationship import Relationship


class KnowledgeGraph:
    """A simple in-memory knowledge graph."""

    def __init__(self) -> None:
        self.entities: dict[str, Entity] = {}
        self.relationships: list[Relationship] = []

    def add_entity(self, entity: Entity) -> None:
        """Add an entity, indexed by its ID."""
        self.entities[entity.id] = entity

    def add_relationship(self, relationship: Relationship) -> None:
        """Store a relationship in the graph."""
        self.relationships.append(relationship)

    def show(self) -> None:
        """Print every relationship in the graph."""
        for relationship in self.relationships:
            print(relationship)

    def get_entity(self, entity_id: str) -> Optional[Entity]:
        """Return an entity by ID, or None when it is not present."""
        return self.entities.get(entity_id)

    def find_entity_by_name(self, name: str) -> Optional[Entity]:
        """Return the first entity whose name matches case-insensitively."""
        requested_name = name.casefold()
        for entity in self.entities.values():
            if entity.name.casefold() == requested_name:
                return entity
        return None

    def find_entities(
        self, entity_type: Optional[str] = None
    ) -> list[Entity]:
        """Return all entities, optionally filtered by type."""
        if entity_type is None:
            return list(self.entities.values())
        requested_type = entity_type.casefold()
        return [
            entity
            for entity in self.entities.values()
            if entity.type.casefold() == requested_type
        ]

    def get_neighbors(
        self, entity_id: str, direction: str = "both"
    ) -> list[dict[str, object]]:
        """Return entities connected to an entity and the connecting edges."""
        valid_directions = {"outgoing", "incoming", "both"}
        if direction not in valid_directions:
            raise ValueError(
                "direction must be 'outgoing', 'incoming', or 'both'"
            )
        if entity_id not in self.entities:
            return []

        neighbors: list[dict[str, object]] = []
        for relationship in self.relationships:
            if (
                direction in {"outgoing", "both"}
                and relationship.source.id == entity_id
            ):
                neighbors.append(
                    {
                        "entity": relationship.target,
                        "relation": relationship.relation_type,
                        "relationship": relationship,
                        "direction": "outgoing",
                    }
                )
            if (
                direction in {"incoming", "both"}
                and relationship.target.id == entity_id
            ):
                neighbors.append(
                    {
                        "entity": relationship.source,
                        "relation": relationship.relation_type,
                        "relationship": relationship,
                        "direction": "incoming",
                    }
                )
        return neighbors

    def find_path(
        self,
        start_entity_id: str,
        end_entity_id: str,
        directed: bool = True,
    ) -> list[dict[str, object]]:
        """Find the shortest entity-and-relationship path using BFS."""
        start = self.get_entity(start_entity_id)
        end = self.get_entity(end_entity_id)
        if start is None or end is None:
            return []
        if start_entity_id == end_entity_id:
            return [{"entity": start}]

        direction = "outgoing" if directed else "both"
        queue = deque([(start_entity_id, [{"entity": start}])])
        visited = {start_entity_id}

        while queue:
            current_id, current_path = queue.popleft()
            for neighbor in self.get_neighbors(current_id, direction):
                entity = neighbor["entity"]
                relationship = neighbor["relationship"]
                if not isinstance(entity, Entity):
                    continue
                if entity.id in visited:
                    continue

                next_path = current_path + [
                    {"relationship": relationship},
                    {"entity": entity},
                ]
                if entity.id == end_entity_id:
                    return next_path
                visited.add(entity.id)
                queue.append((entity.id, next_path))
        return []

    def format_path(self, path: list[dict[str, object]]) -> str:
        """Format a structured path with arrows that preserve edge direction."""
        if not path:
            return "No path found."

        first_entity = path[0].get("entity")
        if not isinstance(first_entity, Entity):
            return "No path found."

        output = first_entity.name
        current_entity = first_entity
        for index in range(1, len(path), 2):
            if index + 1 >= len(path):
                return "No path found."
            relationship = path[index].get("relationship")
            next_entity = path[index + 1].get("entity")
            if not isinstance(relationship, Relationship):
                return "No path found."
            if not isinstance(next_entity, Entity):
                return "No path found."

            if relationship.source.id == current_entity.id:
                output += (
                    f" --[{relationship.relation_type}]--> {next_entity.name}"
                )
            else:
                output += (
                    f" <--[{relationship.relation_type}]-- {next_entity.name}"
                )
            current_entity = next_entity
        return output

    def get_subgraph(
        self,
        center_entity_id: str,
        depth: int = 1,
        direction: str = "both",
    ) -> "KnowledgeGraph":
        """Return a new graph containing nodes reachable within a BFS depth."""
        if depth < 0:
            raise ValueError("depth must be zero or greater")
        if direction not in {"outgoing", "incoming", "both"}:
            raise ValueError(
                "direction must be 'outgoing', 'incoming', or 'both'"
            )

        subgraph = KnowledgeGraph()
        center = self.get_entity(center_entity_id)
        if center is None:
            return subgraph

        subgraph.add_entity(center)
        if depth == 0:
            return subgraph

        queue = deque([(center_entity_id, 0)])
        visited = {center_entity_id}
        added_relationships: set[int] = set()

        while queue:
            current_id, current_depth = queue.popleft()
            if current_depth >= depth:
                continue
            for neighbor in self.get_neighbors(current_id, direction):
                entity = neighbor["entity"]
                relationship = neighbor["relationship"]
                if not isinstance(entity, Entity):
                    continue
                if not isinstance(relationship, Relationship):
                    continue

                subgraph.add_entity(entity)
                relationship_identity = id(relationship)
                if relationship_identity not in added_relationships:
                    subgraph.add_relationship(relationship)
                    added_relationships.add(relationship_identity)

                if entity.id not in visited:
                    visited.add(entity.id)
                    queue.append((entity.id, current_depth + 1))
        return subgraph

    def get_statistics(self) -> dict[str, object]:
        """Return counts for entities, relationships, types, and isolation."""
        entity_types = Counter(
            entity.type.casefold() for entity in self.entities.values()
        )
        relationship_types = Counter(
            relationship.relation_type.casefold()
            for relationship in self.relationships
        )
        connected_ids: set[str] = set()
        for relationship in self.relationships:
            connected_ids.add(relationship.source.id)
            connected_ids.add(relationship.target.id)

        isolated_entities = [
            entity.id
            for entity in self.entities.values()
            if entity.id not in connected_ids
        ]
        return {
            "entity_count": len(self.entities),
            "relationship_count": len(self.relationships),
            "entity_types": dict(entity_types),
            "relationship_types": dict(relationship_types),
            "isolated_entities": isolated_entities,
        }
