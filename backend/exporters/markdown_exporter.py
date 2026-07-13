from pathlib import Path
from typing import Optional, Union

try:
    from ..graph import KnowledgeGraph
except ImportError:  # Support running backend/test_pipeline.py directly.
    from graph import KnowledgeGraph


class MarkdownExporter:
    """Serialize a knowledge graph as readable Markdown."""

    def export(
        self,
        graph: KnowledgeGraph,
        path: Optional[Union[str, Path]] = None,
    ) -> str:
        """Return Markdown and optionally write it to a UTF-8 file."""
        lines = ["# Knowledge Graph", "", "## Entities", ""]
        lines.extend(
            f"- **{entity.name}** (`{entity.type}`) — `{entity.id}`"
            for entity in graph.entities.values()
        )
        lines.extend(["", "## Relationships", ""])
        for relationship in graph.relationships:
            lines.extend(
                [
                    f"### {relationship}",
                    "",
                    f"- Evidence: `{relationship.evidence or 'Unknown'}`",
                    "- Sentence index: "
                    f"{self._display(relationship.sentence_index)}",
                    f"- Source: {relationship.source_name or 'Unknown'}",
                    f"- Timestamp: {relationship.timestamp or 'Unknown'}",
                    f"- Confidence: {self._display(relationship.confidence)}",
                    "",
                ]
            )

        output = "\n".join(lines) + "\n"
        if path is not None:
            Path(path).write_text(output, encoding="utf-8")
        return output

    @staticmethod
    def _display(value: object) -> str:
        """Display missing optional metadata consistently."""
        return "Unknown" if value is None else str(value)
