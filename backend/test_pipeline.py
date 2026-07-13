from pathlib import Path

try:
    from .exporters import JSONExporter, MarkdownExporter
    from .pipeline import SignalGraphPipeline
except ImportError:  # Support running this file directly.
    from exporters import JSONExporter, MarkdownExporter
    from pipeline import SignalGraphPipeline


def run_test() -> None:
    """Run the context-aware pipeline and create both supported exports."""
    text = (
        "OpenAI released GPT-4o in 2024. "
        "Microsoft invested in OpenAI. "
        "GPT-4o works with ChatGPT."
    )

    graph = SignalGraphPipeline().analyze(text, source_name="example.txt")

    expected_relationships = [
        "OpenAI --[released]--> GPT-4o",
        "Microsoft --[invested_in]--> OpenAI",
        "GPT-4o --[works_with]--> ChatGPT",
    ]
    actual_relationships = [str(item) for item in graph.relationships]
    assert actual_relationships == expected_relationships

    released, invested, works_with = graph.relationships
    assert released.evidence == "OpenAI released GPT-4o in 2024."
    assert released.timestamp == "2024"
    assert released.source_name == "example.txt"
    assert released.sentence_index == 0
    assert released.confidence == 1.0

    assert invested.evidence == "Microsoft invested in OpenAI."
    assert invested.sentence_index == 1
    assert invested.source_name == "example.txt"
    assert invested.timestamp is None

    assert works_with.evidence == "GPT-4o works with ChatGPT."
    assert works_with.sentence_index == 2
    assert works_with.source_name == "example.txt"

    project_root = Path(__file__).resolve().parent.parent
    json_output = JSONExporter().export(graph, project_root / "output.json")
    markdown_output = MarkdownExporter().export(graph, project_root / "output.md")

    assert '"evidence": "OpenAI released GPT-4o in 2024."' in json_output
    assert '"sentence_index": 0' in json_output
    assert "### OpenAI --[released]--> GPT-4o" in markdown_output
    assert "- Evidence: `OpenAI released GPT-4o in 2024.`" in markdown_output

    graph.show()


if __name__ == "__main__":
    run_test()
