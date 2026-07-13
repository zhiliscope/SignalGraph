"""Executable tests for graph lookup and exploration algorithms."""

try:
    from .graph import Entity, KnowledgeGraph, Relationship
except ImportError:  # Support running this file directly.
    from graph import Entity, KnowledgeGraph, Relationship


def build_graph() -> KnowledgeGraph:
    """Create a small graph with a three-edge path and an isolated node."""
    graph = KnowledgeGraph()
    microsoft = Entity("microsoft", "Organization", "Microsoft")
    openai = Entity("openai", "Organization", "OpenAI")
    gpt = Entity("gpt", "Technology", "GPT")
    chatgpt = Entity("chatgpt", "Product", "ChatGPT")
    isolated = Entity("isolated", "Topic", "Isolated Topic")
    for entity in (microsoft, openai, gpt, chatgpt, isolated):
        graph.add_entity(entity)

    graph.add_relationship(
        Relationship(
            microsoft,
            "invested_in",
            openai,
            evidence="Microsoft invested in OpenAI.",
            sentence_index=0,
            source_name="example.txt",
            confidence=1.0,
        )
    )
    graph.add_relationship(
        Relationship(
            openai,
            "created",
            gpt,
            evidence="OpenAI created GPT.",
            sentence_index=1,
            source_name="example.txt",
            confidence=1.0,
        )
    )
    graph.add_relationship(
        Relationship(
            gpt,
            "powers",
            chatgpt,
            evidence="GPT powers ChatGPT.",
            sentence_index=2,
            source_name="example.txt",
            confidence=1.0,
        )
    )
    return graph


def run_test() -> None:
    """Verify graph queries, BFS paths, subgraphs, and statistics."""
    graph = build_graph()

    assert graph.get_entity("openai").name == "OpenAI"
    assert graph.get_entity("missing") is None
    assert graph.find_entity_by_name("OPENAI").id == "openai"
    assert graph.find_entity_by_name("unknown") is None
    assert len(graph.find_entities()) == 5
    assert [entity.id for entity in graph.find_entities("organization")] == [
        "microsoft",
        "openai",
    ]

    outgoing = graph.get_neighbors("openai", "outgoing")
    assert len(outgoing) == 1
    assert outgoing[0]["entity"].id == "gpt"
    assert outgoing[0]["direction"] == "outgoing"

    incoming = graph.get_neighbors("openai", "incoming")
    assert len(incoming) == 1
    assert incoming[0]["entity"].id == "microsoft"
    assert incoming[0]["direction"] == "incoming"

    both = graph.get_neighbors("openai")
    assert {neighbor["entity"].id for neighbor in both} == {
        "microsoft",
        "gpt",
    }
    assert graph.get_neighbors("missing") == []
    try:
        graph.get_neighbors("openai", "sideways")
    except ValueError:
        pass
    else:
        raise AssertionError("invalid neighbor direction should raise ValueError")

    directed_path = graph.find_path("microsoft", "chatgpt")
    assert len(directed_path) == 7
    assert graph.format_path(directed_path) == (
        "Microsoft --[invested_in]--> OpenAI --[created]--> GPT "
        "--[powers]--> ChatGPT"
    )
    created_relationship = directed_path[3]["relationship"]
    assert created_relationship.evidence == "OpenAI created GPT."
    assert created_relationship.source_name == "example.txt"

    assert graph.find_path("chatgpt", "microsoft") == []
    undirected_path = graph.find_path(
        "chatgpt", "microsoft", directed=False
    )
    assert len(undirected_path) == 7
    assert graph.format_path(undirected_path) == (
        "ChatGPT <--[powers]-- GPT <--[created]-- OpenAI "
        "<--[invested_in]-- Microsoft"
    )
    assert graph.find_path("microsoft", "isolated") == []
    same_entity_path = graph.find_path("openai", "openai")
    assert len(same_entity_path) == 1
    assert same_entity_path[0]["entity"].id == "openai"
    assert graph.format_path([]) == "No path found."

    depth_zero = graph.get_subgraph("openai", depth=0)
    assert list(depth_zero.entities) == ["openai"]
    assert depth_zero.relationships == []

    depth_one = graph.get_subgraph("openai", depth=1)
    assert set(depth_one.entities) == {"microsoft", "openai", "gpt"}
    assert len(depth_one.relationships) == 2
    assert depth_one.relationships[1].evidence == "OpenAI created GPT."

    depth_two = graph.get_subgraph("openai", depth=2)
    assert set(depth_two.entities) == {
        "microsoft", "openai", "gpt", "chatgpt"
    }
    assert len(depth_two.relationships) == 3
    assert depth_two.relationships[1] is graph.relationships[1]

    try:
        graph.get_subgraph("openai", depth=-1)
    except ValueError:
        pass
    else:
        raise AssertionError("negative depth should raise ValueError")

    cycle = KnowledgeGraph()
    cycle_entities = [Entity(letter, "Topic", letter.upper()) for letter in "abc"]
    for entity in cycle_entities:
        cycle.add_entity(entity)
    for source, target in zip(
        cycle_entities, cycle_entities[1:] + cycle_entities[:1]
    ):
        cycle.add_relationship(Relationship(source, "links_to", target))
    assert len(cycle.find_path("a", "c")) == 5
    assert len(cycle.get_subgraph("a", depth=10).entities) == 3
    assert len(cycle.get_subgraph("a", depth=10).relationships) == 3

    statistics = graph.get_statistics()
    assert statistics["entity_count"] == 5
    assert statistics["relationship_count"] == 3
    assert statistics["entity_types"] == {
        "organization": 2,
        "technology": 1,
        "product": 1,
        "topic": 1,
    }
    assert statistics["relationship_types"] == {
        "invested_in": 1,
        "created": 1,
        "powers": 1,
    }
    assert statistics["isolated_entities"] == ["isolated"]

    print("Graph query tests passed.")


if __name__ == "__main__":
    run_test()
