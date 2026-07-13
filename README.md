## SignalGraph

> **Connect what was never connected.**

SignalGraph turns scattered information into connected knowledge.

Instead of leaving facts isolated across articles, notes, reports, and research papers, SignalGraph discovers explicit relationships between them and organizes everything into a structured network that can be explored, queried, exported, and reused.

Built with deterministic, rule-based extraction, explainable evidence, and zero external AI dependencies.

[![Python 3.9+](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/downloads/)
[![MIT License](https://img.shields.io/badge/license-MIT-yellow.svg)](LICENSE)
![Pure Python](https://img.shields.io/badge/implementation-pure%20Python-blue.svg)
![Zero Dependencies](https://img.shields.io/badge/dependencies-zero-success.svg)
![CLI](https://img.shields.io/badge/interface-CLI-4c8bf5.svg)
![Cross Platform](https://img.shields.io/badge/platform-cross--platform-lightgrey.svg)
![Status: Alpha](https://img.shields.io/badge/status-alpha-orange.svg)
[![Contributions Welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg)](#contributing)

## Highlights

- Deterministic rule-based extraction
- Explainable relationships with source evidence
- In-memory relationship querying
- Pure Python with zero external runtime dependencies

## Example

### Input

```text
Microsoft invested in OpenAI.
OpenAI created GPT.
GPT powers ChatGPT.
```

↓

### Output

```text
Microsoft ──invested_in──▶ OpenAI
OpenAI ──created────────▶ GPT
GPT ──powers───────────▶ ChatGPT
```

SignalGraph connects scattered facts into a structured relationship graph that
can be explored, queried, and reused.

Separate statements become part of one connected information structure instead
of remaining isolated facts.

## Why SignalGraph?

- **Deterministic** — extraction follows explicit, repeatable rules.
- **Lightweight** — the framework has a small standard-library codebase.
- **Explainable** — relationships retain the sentence that produced them.
- **Transparent** — rules, graph models, and query algorithms are inspectable.
- **Reusable** — pipeline components can be imported independently.
- **Pure Python** — the implementation requires Python 3.9 or newer.
- **Zero external models** — analysis does not call model APIs or services.
- **Easy integration** — connected relationships can be queried in Python or
  exchanged as JSON.

## Features

### Extraction

- Parse UTF-8 plain-text and Markdown input.
- Extract named entities with deterministic, rule-based heuristics.
- Extract explicit relationships for `released`, `created`, `developed`,
  `invested_in`, `uses`, `works_with`, `part_of`, `related_to`, and `powers`.
- Preserve the source sentence and sentence index for each relationship.
- Extract the first four-digit year in a relationship sentence as its timestamp.
- Store source names and confidence metadata.
- Keep years as relationship timestamps instead of standalone entities by
  default.

### Graph

- Organize extracted facts in an in-memory directed relationship graph.
- Find entities by ID, name, or type.
- Query incoming, outgoing, or bidirectional neighbors.
- Find shortest directed or undirected paths with breadth-first search.
- Create depth-limited connected subgraphs.
- Calculate entity, relationship, type, and isolation statistics.

### Export

- Export connected relationship structures to JSON.
- Export readable relationship reports to Markdown.
- Reload and validate previously exported SignalGraph JSON.

### CLI

- Analyze direct text or UTF-8 `.txt` and `.md` files.
- Explore paths and neighbors in exported relationship data.
- Display graph statistics.
- Generate and export connected subgraphs.

## Installation

SignalGraph currently runs directly from the repository and has no third-party
runtime dependencies.

```bash
git clone https://github.com/zhiliscope/SignalGraph.git
cd SignalGraph
python3 --version
python3 -m backend.cli --help
```

Python 3.9 or newer is required. Run commands from the repository root.

## Quick Start

### Analyze text

```bash
python3 -m backend.cli analyze --text "Microsoft invested in OpenAI. OpenAI created GPT. GPT powers ChatGPT."
```

### Find the shortest path

```bash
python3 -m backend.cli path output.json microsoft chatgpt
```

### List neighbors

```bash
python3 -m backend.cli neighbors output.json openai --direction both
```

### Show graph statistics

```bash
python3 -m backend.cli stats output.json
```

### Export a subgraph

```bash
python3 -m backend.cli subgraph output.json openai --depth 2 --json subgraph.json --markdown subgraph.md
```

The analyze command creates `output.json` and `output.md` by default.

## Architecture

```text
Raw Text
    │
    ▼
Text Parser
    │
    ▼
Entity Extractor
    │
    ▼
Relationship Extractor
    │
    ▼
Connected Relationship Graph
    ├── JSON Export
    ├── Markdown Export
    └── CLI Queries
```

Parsing, extraction, relationship organization, serialization, and querying are
kept in separate modules so they can be used independently.

## Project Structure

```text
SignalGraph/
├── backend/
│   ├── cli.py                         # Command-line entry point
│   ├── pipeline.py                    # Analysis pipeline orchestration
│   ├── parser/
│   │   └── text_parser.py             # Text and Markdown sentence parsing
│   ├── extractors/
│   │   ├── entity_extractor.py        # Rule-based entity extraction
│   │   └── relationship_extractor.py  # Explicit relationship extraction
│   ├── graph/
│   │   ├── entity.py                  # Entity model
│   │   ├── relationship.py            # Relationship and evidence model
│   │   └── graph.py                   # Graph storage and query algorithms
│   ├── exporters/
│   │   ├── json_exporter.py           # JSON serialization
│   │   ├── json_loader.py             # JSON validation and reconstruction
│   │   └── markdown_exporter.py       # Markdown serialization
│   └── test_*.py                      # Executable test modules
├── docs/
│   └── data-model.md                  # Data-model notes
├── LICENSE
└── README.md
```

## CLI Reference

All commands use the following entry point:

```bash
python3 -m backend.cli COMMAND
```

### `analyze`

Parse text, extract entities and relationships, connect the extracted facts,
and write the enabled output formats.

```bash
python3 -m backend.cli analyze [FILE] [OPTIONS]
```

Exactly one input source is required: a positional `.txt` or `.md` file, or
`--text`.

| Argument | Description | Default |
| --- | --- | --- |
| `FILE` | UTF-8 `.txt` or `.md` input file | — |
| `--text TEXT` | Analyze text supplied directly | — |
| `--json PATH` | JSON output path | `output.json` |
| `--no-json` | Disable JSON output | Off |
| `--markdown PATH` | Markdown output path | `output.md` |
| `--no-markdown` | Disable Markdown output | Off |
| `--source-name NAME` | Override the source name stored on relationships | File name or `command-line-input` |

### `path`

Load a SignalGraph JSON file and find the shortest path between two entity IDs.

```bash
python3 -m backend.cli path GRAPH_JSON START_ENTITY_ID END_ENTITY_ID [--undirected]
```

| Argument | Description |
| --- | --- |
| `GRAPH_JSON` | Previously exported SignalGraph JSON file |
| `START_ENTITY_ID` | Starting entity ID |
| `END_ENTITY_ID` | Destination entity ID |
| `--undirected` | Allow traversal in either relationship direction |

Path searches are directed by default. A missing path prints `No path found.`
and is not treated as a command error.

### `neighbors`

List relationships connected to an entity.

```bash
python3 -m backend.cli neighbors GRAPH_JSON ENTITY_ID [--direction DIRECTION]
```

| Argument | Description | Default |
| --- | --- | --- |
| `GRAPH_JSON` | Previously exported SignalGraph JSON file | — |
| `ENTITY_ID` | Entity whose neighbors should be listed | — |
| `--direction` | `incoming`, `outgoing`, or `both` | `both` |

### `stats`

Display entity counts, relationship counts, type distributions, and isolated
entity IDs.

```bash
python3 -m backend.cli stats GRAPH_JSON
```

### `subgraph`

Build and export the graph reachable around a center entity within a selected
breadth-first depth.

```bash
python3 -m backend.cli subgraph GRAPH_JSON ENTITY_ID [OPTIONS]
```

| Argument | Description | Default |
| --- | --- | --- |
| `GRAPH_JSON` | Previously exported SignalGraph JSON file | — |
| `ENTITY_ID` | Center entity ID | — |
| `--depth INTEGER` | Maximum traversal depth; must be zero or greater | `1` |
| `--direction` | `incoming`, `outgoing`, or `both` | `both` |
| `--json PATH` | Subgraph JSON output path | `subgraph.json` |
| `--markdown PATH` | Subgraph Markdown output path | `subgraph.md` |

Use `python3 -m backend.cli COMMAND --help` for the generated argument reference.

## Python API Example

```python
from backend.exporters import JSONExporter
from backend.pipeline import SignalGraphPipeline

text = (
    "Microsoft invested in OpenAI. "
    "OpenAI created GPT. "
    "GPT powers ChatGPT."
)

pipeline = SignalGraphPipeline()
graph = pipeline.analyze(text, source_name="example.txt")

path = graph.find_path("microsoft", "chatgpt")
print(graph.format_path(path))

for neighbor in graph.get_neighbors("openai", direction="both"):
    print(neighbor["direction"], neighbor["relationship"])

statistics = graph.get_statistics()
print(statistics)

JSONExporter().export(graph, "output.json")
```

Core classes are also available from `backend.graph`, and individual parsers,
extractors, loaders, and exporters can be imported from their respective
packages.

## Current Limitations

- Sentence splitting uses punctuation and line boundaries; it does not perform
  language-aware abbreviation or sentence analysis.
- Entity extraction relies on capitalization, known-name lists, suffixes, and
  naming patterns. Ambiguous entities can be misclassified.
- Relationship extraction supports a fixed set of explicit phrases and active
  constructions. It does not resolve pronouns, aliases, passive voice, or
  implied relationships.
- Only the first four-digit year in a relationship sentence is stored as its
  timestamp. Years are not standalone entities by default.
- Input files are limited to UTF-8 `.txt` and `.md` files. Other document types
  must be converted to text before analysis.
- Graphs are held in memory. JSON and Markdown are the current interchange
  formats.
- Path finding is unweighted and minimizes the number of relationships.
- Entity IDs are normalized from names; alias resolution and entity merging are
  not implemented.
- The exported JSON format does not currently include a schema version or
  migration mechanism.

## Roadmap

### Current

- Core entity, relationship, and graph models
- Deterministic analysis pipeline with evidence preservation
- JSON and Markdown serialization
- Command-line analysis and graph exploration
- Path, neighbor, subgraph, and statistics queries

### Next

- Configurable entity and relationship rules
- Improved sentence parsing and entity classification
- Additional validation and test coverage for graph interchange
- A stable installation and packaging workflow

### Future

- Additional text-based input adapters
- Extensible extraction components
- Expanded temporal and graph-analysis operations
- Stabilized public Python APIs

## Contributing

Issues and pull requests are welcome. Keep changes focused, use only the Python
standard library unless a dependency is explicitly discussed, and include tests
for behavior changes.

Run the complete test suite from the repository root:

```bash
python3 backend/test.py
python3 backend/test_pipeline.py
python3 backend/test_relationship_context.py
python3 backend/test_cli.py
python3 backend/test_graph_queries.py
```

When opening a pull request, describe the behavior change, its limitations, and
the commands used to verify it.

## License

SignalGraph is available under the [MIT License](LICENSE).
