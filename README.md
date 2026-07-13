# SignalGraph

> A knowledge graph engine for exploring relationships and patterns in public information.

SignalGraph transforms scattered public information into connected knowledge graphs, helping users discover hidden relationships, emerging trends, and structures behind complex information systems.

## Overview

The world produces massive amounts of information every day, but meaningful connections are often hidden.

SignalGraph explores how information can be collected, structured, and represented as a dynamic graph.

## Usage

Analyze a UTF-8 TXT or Markdown file:

```bash
python3 -m backend.cli analyze example.txt
```

Analyze text directly:

```bash
python3 -m backend.cli analyze --text "OpenAI released GPT-4o in 2024."
```

Choose the JSON and Markdown output paths:

```bash
python3 -m backend.cli analyze example.md --json result.json --markdown result.md
```

SignalGraph currently supports `.txt` and `.md` input files. By default, it
creates `output.json` and `output.md`; use `--no-json` or `--no-markdown` to
disable either format.

## Graph Exploration

Explore a previously exported SignalGraph JSON file:

```bash
python3 -m backend.cli path output.json microsoft chatgpt
python3 -m backend.cli neighbors output.json openai --direction both
python3 -m backend.cli stats output.json
python3 -m backend.cli subgraph output.json openai --depth 2
```

The same graph queries are available through Python:

```python
from backend.pipeline import SignalGraphPipeline

text = (
    "Microsoft invested in OpenAI. "
    "OpenAI created GPT. "
    "GPT powers ChatGPT."
)
graph = SignalGraphPipeline().analyze(text)
path = graph.find_path("microsoft", "chatgpt")
print(graph.format_path(path))
```

Instead of viewing information as isolated pieces, SignalGraph focuses on understanding:

- How entities are connected
- How information evolves over time
- How patterns emerge from complex systems

## Concept

```
Public Information

        ↓

Information Extraction

        ↓

Entity & Relationship Discovery

        ↓

Knowledge Graph

        ↓

Insight & Visualization
```

## Features

- [x] TXT and Markdown parsing
- [x] Deterministic entity and relationship extraction
- [x] Relationship evidence and source context
- [x] In-memory knowledge graph generation
- [x] JSON and Markdown export
- [x] Graph path, neighbor, subgraph, and statistics queries
- [x] Command-line interface

## Example

Input:

```
A collection of public articles, discussions, and documents
```

Output:

```
        Entity A

           |
        relates to

           |

        Entity B

           |
        mentioned in

           |

        Entity C
```

SignalGraph aims to reveal the hidden structure behind fragmented information.

## Technology Stack

- Python standard library
- Deterministic text processing
- Knowledge graph data structures
- Breadth-first graph algorithms

## Roadmap

### Phase 1 — Graph Foundation

- Design core data structures
- Create entity and relationship models
- Build graph generation engine

### Phase 2 — Information Processing

- Add text processing pipeline
- Extract entities and relationships
- Process public information sources

### Phase 3 — Extraction Expansion

- Add more relationship patterns
- Support additional text-based document formats

### Phase 4 — Analysis Layer

- Add configurable extraction rules
- Expand graph analysis capabilities

## Why SignalGraph?

Modern information systems are becoming increasingly complex.

SignalGraph is an exploration of how we can better understand these systems by connecting information, relationships, and context.

## Contributing

Contributions, ideas, and discussions are welcome.

## License

MIT License
