import re

try:
    from ..graph import Entity
except ImportError:  # Support running backend/test_pipeline.py directly.
    from graph import Entity


class EntityExtractor:
    """Extract likely named entities using deterministic naming rules."""

    _name_pattern = re.compile(
        r"\b[A-Z][A-Za-z0-9.+#]*(?:-[A-Za-z0-9]+)?"
        r"(?:\s+(?:(?:of|the|and)|[A-Z][A-Za-z0-9.+#]*)){0,4}\b"
    )
    _year_pattern = re.compile(r"\b(?:1[0-9]{3}|20[0-9]{2}|21[0-9]{2})\b")
    _organizations = {
        "Amazon",
        "Apple",
        "Google",
        "Meta",
        "Microsoft",
        "NASA",
        "OpenAI",
        "UNESCO",
        "United Nations",
    }
    _technologies = {
        "ChatGPT",
        "GPT",
        "Java",
        "JavaScript",
        "Linux",
        "Python",
    }
    _locations = {
        "Africa",
        "Asia",
        "Beijing",
        "Berlin",
        "China",
        "Europe",
        "India",
        "London",
        "New York",
        "Paris",
        "Shanghai",
        "Tokyo",
        "United Kingdom",
        "United States",
    }
    _organization_suffixes = (
        "Association",
        "Company",
        "Corporation",
        "Foundation",
        "Group",
        "Institute",
        "Laboratory",
        "Labs",
        "Ltd",
        "University",
    )

    def extract(self, sentences: list[str]) -> list[Entity]:
        """Return unique entities in their first-seen order."""
        entities: dict[str, Entity] = {}

        for sentence in sentences:
            candidates = [
                match.group() for match in self._name_pattern.finditer(sentence)
            ]
            candidates.extend(self._year_pattern.findall(sentence))

            for name in candidates:
                name = name.strip()
                entity_id = self._make_id(name)
                if entity_id and entity_id not in entities:
                    entity_type = self._classify(name, sentence)
                    entities[entity_id] = Entity(entity_id, entity_type, name)

        return list(entities.values())

    @staticmethod
    def _make_id(name: str) -> str:
        """Create a stable, readable ID from an entity name."""
        return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")

    def _classify(self, name: str, sentence: str) -> str:
        """Assign a broad type using conservative deterministic rules."""
        if self._year_pattern.fullmatch(name):
            return "Year"
        if name in self._organizations or name.endswith(
            self._organization_suffixes
        ):
            return "Organization"
        if name in self._locations:
            return "Location"
        if name in self._technologies or self._looks_like_technology(name):
            return "Technology"
        if name.startswith("Project ") or re.search(
            rf"\bproject\s+{re.escape(name)}\b", sentence, re.IGNORECASE
        ):
            return "Project"
        if self._looks_like_person(name):
            return "Person"
        return "Topic"

    @staticmethod
    def _looks_like_technology(name: str) -> bool:
        """Recognize common product-style names without a fixed vocabulary."""
        return bool(
            re.search(r"\d", name)
            or re.fullmatch(r"[A-Z]{2,}(?:-[A-Za-z0-9]+)?", name)
            or re.search(r"[a-z][A-Z]", name)
        )

    @staticmethod
    def _looks_like_person(name: str) -> bool:
        """Recognize conventional two- or three-part personal names."""
        parts = name.split()
        return 2 <= len(parts) <= 3 and all(part.istitle() for part in parts)
