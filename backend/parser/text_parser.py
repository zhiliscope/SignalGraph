import re


class TextParser:
    """Convert raw text or simple Markdown into clean sentences."""

    _sentence_boundary = re.compile(r"(?<=[.!?])\s+|\n+")

    def parse(self, text: str) -> list[str]:
        """Return non-empty sentences with normalized whitespace."""
        if not isinstance(text, str):
            raise TypeError("text must be a string")

        cleaned_lines: list[str] = []
        for line in text.splitlines():
            line = re.sub(r"^\s{0,3}#{1,6}\s+", "", line)
            line = re.sub(r"^\s*(?:[-*+] |\d+[.)]\s+)", "", line)
            line = re.sub(r"!\[([^]]*)\]\([^)]+\)", r"\1", line)
            line = re.sub(r"\[([^]]+)\]\([^)]+\)", r"\1", line)
            line = re.sub(r"[*_`~]", "", line)
            line = re.sub(r"\s+", " ", line).strip()
            if line:
                cleaned_lines.append(line)

        normalized = "\n".join(cleaned_lines)
        return [
            sentence.strip()
            for sentence in self._sentence_boundary.split(normalized)
            if sentence.strip()
        ]
