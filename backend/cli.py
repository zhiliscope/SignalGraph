"""Command-line interface for SignalGraph."""

import argparse
from pathlib import Path
from typing import Optional, Sequence

from .exporters import JSONExporter, JSONLoader, MarkdownExporter
from .graph import KnowledgeGraph
from .pipeline import SignalGraphPipeline


def build_parser() -> argparse.ArgumentParser:
    """Create and configure the command-line argument parser."""
    parser = argparse.ArgumentParser(
        prog="python3 -m backend.cli",
        description="Transform text into a SignalGraph knowledge graph.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    analyze_parser = subparsers.add_parser(
        "analyze", help="Analyze a TXT or Markdown file, or direct text."
    )
    input_group = analyze_parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument(
        "file", nargs="?", help="Path to a UTF-8 .txt or .md file."
    )
    input_group.add_argument("--text", help="Text to analyze directly.")

    json_group = analyze_parser.add_mutually_exclusive_group()
    json_group.add_argument(
        "--json", dest="json_path", default="output.json", metavar="PATH"
    )
    json_group.add_argument(
        "--no-json", action="store_true", help="Disable JSON output."
    )

    markdown_group = analyze_parser.add_mutually_exclusive_group()
    markdown_group.add_argument(
        "--markdown",
        dest="markdown_path",
        default="output.md",
        metavar="PATH",
    )
    markdown_group.add_argument(
        "--no-markdown", action="store_true", help="Disable Markdown output."
    )

    analyze_parser.add_argument(
        "--source-name", help="Override the source name stored as evidence."
    )

    path_parser = subparsers.add_parser(
        "path", help="Find the shortest path between two entities."
    )
    path_parser.add_argument("graph_json", help="SignalGraph JSON file.")
    path_parser.add_argument("start_entity_id")
    path_parser.add_argument("end_entity_id")
    path_parser.add_argument(
        "--undirected",
        action="store_true",
        help="Allow traversal in either relationship direction.",
    )

    neighbors_parser = subparsers.add_parser(
        "neighbors", help="List entities neighboring an entity."
    )
    neighbors_parser.add_argument("graph_json", help="SignalGraph JSON file.")
    neighbors_parser.add_argument("entity_id")
    neighbors_parser.add_argument(
        "--direction",
        choices=("incoming", "outgoing", "both"),
        default="both",
    )

    stats_parser = subparsers.add_parser(
        "stats", help="Show graph statistics."
    )
    stats_parser.add_argument("graph_json", help="SignalGraph JSON file.")

    subgraph_parser = subparsers.add_parser(
        "subgraph", help="Export a connected subgraph around an entity."
    )
    subgraph_parser.add_argument("graph_json", help="SignalGraph JSON file.")
    subgraph_parser.add_argument("entity_id")
    subgraph_parser.add_argument("--depth", type=int, default=1)
    subgraph_parser.add_argument(
        "--direction",
        choices=("incoming", "outgoing", "both"),
        default="both",
    )
    subgraph_parser.add_argument(
        "--json", dest="json_path", default="subgraph.json", metavar="PATH"
    )
    subgraph_parser.add_argument(
        "--markdown",
        dest="markdown_path",
        default="subgraph.md",
        metavar="PATH",
    )
    return parser


def _load_input(args: argparse.Namespace) -> tuple[str, str]:
    """Load and validate file or direct-text input."""
    if args.file is not None:
        path = Path(args.file)
        if not path.exists():
            raise ValueError(f"Input file does not exist: {path}")
        if not path.is_file():
            raise ValueError(f"Input path is not a file: {path}")
        if path.suffix.lower() not in {".txt", ".md"}:
            raise ValueError(
                "Unsupported file extension. SignalGraph currently supports "
                ".txt and .md files."
            )
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeError) as error:
            raise ValueError(f"Could not read input file: {error}") from error
        source_name = args.source_name or path.name
    else:
        text = args.text
        source_name = args.source_name or "command-line-input"

    if not text or not text.strip():
        raise ValueError("Input text is empty.")
    return text, source_name


def _export_results(
    graph: KnowledgeGraph, args: argparse.Namespace
) -> list[str]:
    """Write enabled output formats and return their displayed paths."""
    created_files: list[str] = []
    try:
        if not args.no_json:
            JSONExporter().export(graph, args.json_path)
            created_files.append(args.json_path)
        if not args.no_markdown:
            MarkdownExporter().export(graph, args.markdown_path)
            created_files.append(args.markdown_path)
    except (OSError, UnicodeError) as error:
        raise ValueError(f"Could not write output file: {error}") from error
    return created_files


def _print_summary(
    graph: KnowledgeGraph, source_name: str, files: list[str]
) -> None:
    """Print a concise analysis summary for command-line users."""
    print("SignalGraph Analysis Complete")
    print()
    print(f"Source: {source_name}")
    print(f"Entities: {len(graph.entities)}")
    print(f"Relationships: {len(graph.relationships)}")
    print()

    if graph.relationships:
        print("Relationships:")
        print()
        for relationship in graph.relationships:
            print(relationship)
    else:
        print("No explicit supported relationships were detected.")

    if files:
        print()
        print("Files created:")
        print()
        for path in files:
            print(f"- {path}")


def _load_graph(path: str) -> KnowledgeGraph:
    """Load a graph for an exploration command."""
    return JSONLoader().load(path)


def _run_path(args: argparse.Namespace) -> None:
    """Find and print a shortest graph path."""
    graph = _load_graph(args.graph_json)
    path = graph.find_path(
        args.start_entity_id,
        args.end_entity_id,
        directed=not args.undirected,
    )
    print(graph.format_path(path))


def _run_neighbors(args: argparse.Namespace) -> None:
    """Print readable neighbor results for one entity."""
    graph = _load_graph(args.graph_json)
    entity = graph.get_entity(args.entity_id)
    neighbors = graph.get_neighbors(args.entity_id, args.direction)
    if entity is None or not neighbors:
        print("No neighbors found.")
        return

    print(f"Neighbors for {entity.name}:")
    for neighbor in neighbors:
        print(f"- {neighbor['direction']}: {neighbor['relationship']}")


def _run_stats(args: argparse.Namespace) -> None:
    """Print readable graph statistics."""
    statistics = _load_graph(args.graph_json).get_statistics()
    print("Graph Statistics")
    print()
    print(f"Entities: {statistics['entity_count']}")
    print(f"Relationships: {statistics['relationship_count']}")
    print()
    print("Entity types:")
    entity_types = statistics["entity_types"]
    if isinstance(entity_types, dict) and entity_types:
        for entity_type, count in entity_types.items():
            print(f"- {entity_type}: {count}")
    else:
        print("- None")
    print()
    print("Relationship types:")
    relationship_types = statistics["relationship_types"]
    if isinstance(relationship_types, dict) and relationship_types:
        for relation_type, count in relationship_types.items():
            print(f"- {relation_type}: {count}")
    else:
        print("- None")
    print()
    print("Isolated entities:")
    isolated_entities = statistics["isolated_entities"]
    if isinstance(isolated_entities, list) and isolated_entities:
        for entity_id in isolated_entities:
            print(f"- {entity_id}")
    else:
        print("- None")


def _run_subgraph(args: argparse.Namespace) -> None:
    """Build and export a connected subgraph."""
    graph = _load_graph(args.graph_json)
    subgraph = graph.get_subgraph(
        args.entity_id, depth=args.depth, direction=args.direction
    )
    try:
        JSONExporter().export(subgraph, args.json_path)
        MarkdownExporter().export(subgraph, args.markdown_path)
    except (OSError, UnicodeError) as error:
        raise ValueError(f"Could not write output file: {error}") from error

    print("Subgraph Export Complete")
    print()
    print(f"Center: {args.entity_id}")
    print(f"Depth: {args.depth}")
    print(f"Entities: {len(subgraph.entities)}")
    print(f"Relationships: {len(subgraph.relationships)}")
    print()
    print("Files created:")
    print(f"- {args.json_path}")
    print(f"- {args.markdown_path}")


def main(argv: Optional[Sequence[str]] = None) -> int:
    """Run the SignalGraph command-line interface."""
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        if args.command == "analyze":
            text, source_name = _load_input(args)
            graph = SignalGraphPipeline().analyze(text, source_name=source_name)
            created_files = _export_results(graph, args)
            _print_summary(graph, source_name, created_files)
        elif args.command == "path":
            _run_path(args)
        elif args.command == "neighbors":
            _run_neighbors(args)
        elif args.command == "stats":
            _run_stats(args)
        elif args.command == "subgraph":
            _run_subgraph(args)
    except ValueError as error:
        parser.error(str(error))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
