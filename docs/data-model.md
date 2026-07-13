# SignalGraph Data Model

## Overview

SignalGraph represents public information as a knowledge graph.

The core idea is to transform scattered information into connected entities and relationships.

The graph consists of three fundamental components:

- Entity (Node)
- Relationship (Edge)
- Source (Information Origin)

---

# Entity (Node)

An Entity represents an object that exists in the information system.

Examples:

- Person
- Organization
- Project
- Technology
- Topic
- Document
- Event

## Entity Structure

```json
{
  "id": "openai",
  "type": "organization",
  "name": "OpenAI"
}
```

Fields:

| Field | Description |
|------|-------------|
| id | Unique identifier |
| type | Category of the entity |
| name | Display name |

---

# Relationship (Edge)

A Relationship describes the connection between two entities.

Examples:

- created
- developed
- mentioned
- references
- related_to
- influenced

## Relationship Structure

```json
{
  "source": "openai",
  "relation": "created",
  "target": "gpt"
}
```

Fields:

| Field | Description |
|------|-------------|
| source | Starting entity |
| relation | Type of connection |
| target | Connected entity |

---

# Source

A Source represents where information is collected from.

Examples:

- Article
- Repository
- Research Paper
- Discussion
- Dataset

## Source Structure

```json
{
  "type": "article",
  "title": "Example Article",
  "url": "https://example.com",
  "timestamp": "2026-01-01"
}
```

Fields:

| Field | Description |
|------|-------------|
| type | Source category |
| title | Source title |
| url | Original location |
| timestamp | Published time |

---

# Graph Example

A simple information graph:

```
        OpenAI

          |
       created

          |

         GPT

          |
       mentioned

          |

       Article
```

The same structure can represent different systems:

## Technology Ecosystem

```
Company

   |
develops

   |

Technology

   |
used_by

   |

Project
```

## Research Network

```
Paper A

   |
cites

   |

Paper B
```

## Security Intelligence

```
Domain

   |
hosts

   |

Service

   |
affected_by

   |

Vulnerability
```

---

# Design Principles

## 1. Information First

SignalGraph focuses on understanding information relationships rather than storing isolated data.

## 2. Flexible Structure

The same graph model should support different domains.

## 3. Explainable Connections

Every relationship should have a clear source and meaning.

---

# Future Extensions

Possible improvements:

- Confidence scoring
- Time-based relationship changes
- AI-assisted entity extraction
- Graph visualization
- Pattern discovery
