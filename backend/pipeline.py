from typing import Optional

try:
    from .extractors import EntityExtractor, RelationshipExtractor
    from .graph import KnowledgeGraph
    from .parser import TextParser
except ImportError:  # Support running backend/test_pipeline.py directly.
    from extractors import EntityExtractor, RelationshipExtractor
    from graph import KnowledgeGraph
    from parser import TextParser


class SignalGraphPipeline:
    """Run parsing, extraction, and graph construction in sequence."""

    def __init__(
        self,
        parser: Optional[TextParser] = None,
        entity_extractor: Optional[EntityExtractor] = None,
        relationship_extractor: Optional[RelationshipExtractor] = None,
    ) -> None:
        self.parser = parser or TextParser()
        self.entity_extractor = entity_extractor or EntityExtractor()
        self.relationship_extractor = (
            relationship_extractor or RelationshipExtractor()
        )

    def analyze(
        self, text: str, source_name: Optional[str] = None
    ) -> KnowledgeGraph:
        """Transform raw text into an in-memory knowledge graph."""
        sentences = self.parser.parse(text)
        entities = self.entity_extractor.extract(sentences)
        relationships = self.relationship_extractor.extract(
            sentences, entities, source_name=source_name
        )

        graph = KnowledgeGraph()
        for entity in entities:
            graph.add_entity(entity)
        for relationship in relationships:
            graph.add_relationship(relationship)
        return graph
