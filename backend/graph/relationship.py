from typing import Optional

from .entity import Entity


class Relationship:
    """A connection between two entities in the knowledge graph."""

    def __init__(
        self,
        source: Entity,
        relation_type: str,
        target: Entity,
        evidence: Optional[str] = None,
        sentence_index: Optional[int] = None,
        source_name: Optional[str] = None,
        timestamp: Optional[str] = None,
        confidence: Optional[float] = None,
    ) -> None:
        if confidence is not None:
            is_number = isinstance(confidence, (int, float))
            if not is_number or isinstance(confidence, bool):
                raise ValueError("confidence must be a number between 0.0 and 1.0")
            if not 0.0 <= confidence <= 1.0:
                raise ValueError("confidence must be between 0.0 and 1.0")

        self.source = source
        self.relation_type = relation_type
        self.target = target
        self.evidence = evidence
        self.sentence_index = sentence_index
        self.source_name = source_name
        self.timestamp = timestamp
        self.confidence = confidence

    def __repr__(self) -> str:
        return (
            f"{self.source.name} --[{self.relation_type}]--> "
            f"{self.target.name}"
        )

    def to_dict(self) -> dict[str, object]:
        """Return the relationship and its provenance as a dictionary."""
        return {
            "source": self.source.id,
            "relation": self.relation_type,
            "target": self.target.id,
            "evidence": self.evidence,
            "sentence_index": self.sentence_index,
            "source_name": self.source_name,
            "timestamp": self.timestamp,
            "confidence": self.confidence,
        }
