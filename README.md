# SignalGraph

> Transform unstructured information into structured knowledge.

SignalGraph is an open-source Python framework for decomposing unstructured
information into entities, relationships, evidence, and knowledge graphs.

Instead of focusing on a specific domain, SignalGraph provides a reusable way
to understand complex information through structured decomposition. It can
process news articles, research papers, technical documents, historical events,
notes, Markdown, and plain text.

## Philosophy

Information is often fragmented. SignalGraph aims to answer questions such as:

- What are the important entities?
- How are they connected?
- What evidence supports each relationship?
- When did an explicitly stated event happen?
- Where did the information come from?

The goal is not simply to generate a graph. The goal is to decompose information
into a structured representation that can be explored, analyzed, and reused.

## How It Works

```text
Raw text
   ↓
Text parsing
   ↓
Entity and relationship extraction
   ↓
Knowledge graph with source evidence
   ↓
JSON or Markdown export
```

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

## Example

Input:

```text
Microsoft invested in OpenAI.
OpenAI created GPT.
GPT powers ChatGPT.
```

Output:

```text
Microsoft --[invested_in]--> OpenAI
OpenAI --[created]--> GPT
GPT --[powers]--> ChatGPT
```

## Features

- TXT and Markdown parsing
- Deterministic entity and relationship extraction
- Relationship evidence, source context, timestamps, and confidence
- In-memory knowledge graph generation
- JSON loading and export
- Markdown export
- Directed and undirected path queries
- Neighbor, connected-subgraph, and statistics queries
- Command-line interface

## Project Goals

SignalGraph is domain-independent and designed for public information such as:

- News and articles
- Research papers and books
- Technical documentation and GitHub projects
- Historical events
- Notes and plain text

## Current Status

SignalGraph is in early development at v0.1. The core graph, deterministic
analysis pipeline, evidence preservation, exporters, JSON loader, command-line
interface, and graph exploration engine are implemented.

## Roadmap

- Add configurable extraction rules
- Support additional text-based document formats
- Expand temporal and graph analysis
- Stabilize the public Python API
- Add a plugin architecture

## Technology

- Python standard library
- Deterministic text processing
- Knowledge graph data structures
- Breadth-first graph algorithms

## Contributing

Contributions, discussions, and ideas are welcome.

## License

MIT License
