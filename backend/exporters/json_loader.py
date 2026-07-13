"""Load knowledge graphs from SignalGraph JSON exports."""

import json
from pathlib import Path
from typing import Optional, Union

try:
    from ..graph import Entity, KnowledgeGraph, Relationship
except ImportError:  # Support direct test execution.
    from graph import Entity, KnowledgeGraph, Relationship


class JSONLoader:
    """Validate and reconstruct a knowledge graph from JSON."""

    def load(self, path: Union[str, Path]) -> KnowledgeGraph:
        """Read a UTF-8 JSON file and return its knowledge graph."""
        file_path = Path(path)
        try:
            content = file_path.read_text(encoding="utf-8")
        except (OSError, UnicodeError) as error:
            raise ValueError(f"Could not read graph JSON: {error}") from error
        return self.loads(content)

    def loads(self, content: str) -> KnowledgeGraph:
        """Validate JSON text and reconstruct its entities and relationships."""
        try:
            data = json.loads(content)
        except json.JSONDecodeError as error:
            raise ValueError(f"Invalid graph JSON: {error.msg}") from error

        if not isinstance(data, dict):
            raise ValueError("Invalid graph JSON: root value must be an object")
        entities_data = data.get("entities")
        relationships_data = data.get("relationships")
        if not isinstance(entities_data, list):
            raise ValueError("Invalid graph JSON: 'entities' must be a list")
        if not isinstance(relationships_data, list):
            raise ValueError(
                "Invalid graph JSON: 'relationships' must be a list"
            )

        graph = KnowledgeGraph()
        for index, item in enumerate(entities_data):
            entity = self._load_entity(item, index)
            if entity.id in graph.entities:
                raise ValueError(f"Duplicate entity ID: {entity.id}")
            graph.add_entity(entity)

        for index, item in enumerate(relationships_data):
            graph.add_relationship(self._load_relationship(item, index, graph))
        return graph

    @staticmethod
    def _required_string(item: dict, field: str, context: str) -> str:
        value = item.get(field)
        if not isinstance(value, str) or not value:
            raise ValueError(
                f"{context} field '{field}' must be a non-empty string"
            )
        return value

    def _load_entity(self, item: object, index: int) -> Entity:
        context = f"Entity at index {index}"
        if not isinstance(item, dict):
            raise ValueError(f"{context} must be an object")
        entity_id = self._required_string(item, "id", context)
        entity_type = self._required_string(item, "type", context)
        name = self._required_string(item, "name", context)
        return Entity(entity_id, entity_type, name)

    def _load_relationship(
        self, item: object, index: int, graph: KnowledgeGraph
    ) -> Relationship:
        context = f"Relationship at index {index}"
        if not isinstance(item, dict):
            raise ValueError(f"{context} must be an object")

        source_id = self._required_string(item, "source", context)
        relation = self._required_string(item, "relation", context)
        target_id = self._required_string(item, "target", context)
        source = graph.get_entity(source_id)
        target = graph.get_entity(target_id)
        if source is None:
            raise ValueError(f"{context} references unknown source: {source_id}")
        if target is None:
            raise ValueError(f"{context} references unknown target: {target_id}")

        evidence = self._optional_string(item, "evidence", context)
        source_name = self._optional_string(item, "source_name", context)
        timestamp = self._optional_string(item, "timestamp", context)
        sentence_index = item.get("sentence_index")
        if sentence_index is not None and (
            not isinstance(sentence_index, int)
            or isinstance(sentence_index, bool)
        ):
            raise ValueError(
                f"{context} field 'sentence_index' must be an integer or null"
            )

        confidence = item.get("confidence")
        if confidence is not None and (
            not isinstance(confidence, (int, float))
            or isinstance(confidence, bool)
        ):
            raise ValueError(
                f"{context} field 'confidence' must be a number or null"
            )

        try:
            return Relationship(
                source,
                relation,
                target,
                evidence=evidence,
                sentence_index=sentence_index,
                source_name=source_name,
                timestamp=timestamp,
                confidence=confidence,
            )
        except ValueError as error:
            raise ValueError(f"{context}: {error}") from error

    @staticmethod
    def _optional_string(
        item: dict, field: str, context: str
    ) -> Optional[str]:
        value = item.get(field)
        if value is not None and not isinstance(value, str):
            raise ValueError(
                f"{context} field '{field}' must be a string or null"
            )
        return value
