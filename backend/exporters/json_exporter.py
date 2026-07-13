import json
from pathlib import Path
from typing import Optional, Union

try:
    from ..graph import KnowledgeGraph
except ImportError:  # Support running backend/test_pipeline.py directly.
    from graph import KnowledgeGraph


class JSONExporter:
    """Serialize a knowledge graph as JSON."""

    def export(
        self,
        graph: KnowledgeGraph,
        path: Optional[Union[str, Path]] = None,
    ) -> str:
        """Return JSON and optionally write it to a UTF-8 file."""
        data = {
            "entities": [
                {"id": entity.id, "type": entity.type, "name": entity.name}
                for entity in graph.entities.values()
            ],
            "relationships": [
                relationship.to_dict() for relationship in graph.relationships
            ],
        }
        output = json.dumps(data, indent=2, ensure_ascii=False)
        if path is not None:
            Path(path).write_text(output + "\n", encoding="utf-8")
        return output
