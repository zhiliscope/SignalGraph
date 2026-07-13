try:
    from .graph import Entity, Relationship
except ImportError:  # Support running this file directly.
    from graph import Entity, Relationship


def run_test() -> None:
    """Verify relationship metadata and backward compatibility."""
    openai = Entity("openai", "Organization", "OpenAI")
    gpt = Entity("gpt-4o", "Technology", "GPT-4o")

    old_style = Relationship(openai, "released", gpt)
    assert str(old_style) == "OpenAI --[released]--> GPT-4o"
    assert old_style.evidence is None
    assert old_style.confidence is None

    contextual = Relationship(
        openai,
        "released",
        gpt,
        evidence="OpenAI released GPT-4o in 2024.",
        sentence_index=0,
        source_name="example.txt",
        timestamp="2024",
        confidence=1.0,
    )
    assert contextual.evidence == "OpenAI released GPT-4o in 2024."
    assert contextual.sentence_index == 0
    assert contextual.source_name == "example.txt"
    assert contextual.timestamp == "2024"
    assert contextual.confidence == 1.0
    assert contextual.to_dict() == {
        "source": "openai",
        "relation": "released",
        "target": "gpt-4o",
        "evidence": "OpenAI released GPT-4o in 2024.",
        "sentence_index": 0,
        "source_name": "example.txt",
        "timestamp": "2024",
        "confidence": 1.0,
    }

    for invalid_confidence in (-0.1, 1.1, "high"):
        try:
            Relationship(
                openai, "released", gpt, confidence=invalid_confidence
            )
        except ValueError:
            pass
        else:
            raise AssertionError("invalid confidence should raise ValueError")

    for valid_confidence in (0.0, 0.5, 1.0):
        relationship = Relationship(
            openai, "released", gpt, confidence=valid_confidence
        )
        assert relationship.confidence == valid_confidence

    print("Relationship context tests passed.")


if __name__ == "__main__":
    run_test()
