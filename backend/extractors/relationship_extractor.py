import re
from typing import Optional

try:
    from ..graph import Entity, Relationship
except ImportError:  # Support running backend/test_pipeline.py directly.
    from graph import Entity, Relationship


class RelationshipExtractor:
    """Extract relationships that are explicitly written in a sentence."""

    _relation_pattern = re.compile(
        r"\b(?P<relation>invested in|works with|part of|related to|"
        r"released|created|developed|uses|powers)\b",
        re.IGNORECASE,
    )

    def extract(
        self,
        sentences: list[str],
        entities: list[Entity],
        source_name: Optional[str] = None,
    ) -> list[Relationship]:
        """Return explicit relationships with sentence-level provenance."""
        relationships: list[Relationship] = []
        seen: set[tuple[str, str, str]] = set()

        for sentence_index, sentence in enumerate(sentences):
            for match in self._relation_pattern.finditer(sentence):
                source = self._find_source(sentence[:match.start()], entities)
                target = self._find_target(sentence[match.end():], entities)
                relation_type = match.group("relation").lower().replace(" ", "_")

                if source is None or target is None or source.id == target.id:
                    continue

                key = (source.id, relation_type, target.id)
                if key not in seen:
                    year_match = re.search(r"\b\d{4}\b", sentence)
                    relationships.append(
                        Relationship(
                            source,
                            relation_type,
                            target,
                            evidence=sentence,
                            sentence_index=sentence_index,
                            source_name=source_name,
                            timestamp=year_match.group() if year_match else None,
                            confidence=1.0,
                        )
                    )
                    seen.add(key)

        return relationships

    @staticmethod
    def _entity_matches(
        text: str, entities: list[Entity]
    ) -> list[tuple[int, Entity]]:
        """Find entities mentioned as complete names in a text fragment."""
        matches: list[tuple[int, Entity]] = []
        for entity in entities:
            pattern = re.compile(
                rf"(?<!\w){re.escape(entity.name)}(?!\w)", re.IGNORECASE
            )
            for match in pattern.finditer(text):
                matches.append((match.start(), entity))
        return matches

    def _find_source(
        self, text: str, entities: list[Entity]
    ) -> Optional[Entity]:
        matches = self._entity_matches(text, entities)
        return max(matches, key=lambda item: item[0])[1] if matches else None

    def _find_target(
        self, text: str, entities: list[Entity]
    ) -> Optional[Entity]:
        matches = self._entity_matches(text, entities)
        return min(matches, key=lambda item: item[0])[1] if matches else None
