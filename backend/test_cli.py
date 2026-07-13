"""Executable integration tests for the SignalGraph CLI."""

import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile


PROJECT_ROOT = Path(__file__).resolve().parent.parent


def run_cli(
    arguments: list[str], working_directory: Path
) -> subprocess.CompletedProcess:
    """Run the CLI in an isolated directory and capture its output."""
    environment = os.environ.copy()
    environment["PYTHONPATH"] = str(PROJECT_ROOT)
    return subprocess.run(
        [sys.executable, "-B", "-m", "backend.cli", *arguments],
        cwd=working_directory,
        env=environment,
        capture_output=True,
        text=True,
        check=False,
    )


def run_test() -> None:
    """Verify successful CLI flows, output flags, and normal errors."""
    with tempfile.TemporaryDirectory() as temporary_directory:
        temp_path = Path(temporary_directory)

        direct = run_cli(
            ["analyze", "--text", "OpenAI released GPT-4o in 2024."],
            temp_path,
        )
        assert direct.returncode == 0, direct.stderr
        assert "SignalGraph Analysis Complete" in direct.stdout
        assert "Source: command-line-input" in direct.stdout
        assert "OpenAI --[released]--> GPT-4o" in direct.stdout
        assert (temp_path / "output.json").is_file()
        assert (temp_path / "output.md").is_file()
        exported = json.loads((temp_path / "output.json").read_text("utf-8"))
        assert exported["relationships"][0]["source_name"] == "command-line-input"

        text_file = temp_path / "example.txt"
        text_file.write_text("Microsoft invested in OpenAI.", encoding="utf-8")
        txt_result = run_cli(
            ["analyze", str(text_file), "--no-json", "--no-markdown"],
            temp_path,
        )
        assert txt_result.returncode == 0, txt_result.stderr
        assert "Source: example.txt" in txt_result.stdout
        assert "Microsoft --[invested_in]--> OpenAI" in txt_result.stdout

        markdown_file = temp_path / "notes.md"
        markdown_file.write_text(
            "# Notes\n\n- GPT-4o works with ChatGPT.", encoding="utf-8"
        )
        md_result = run_cli(
            ["analyze", str(markdown_file), "--no-json", "--no-markdown"],
            temp_path,
        )
        assert md_result.returncode == 0, md_result.stderr
        assert "GPT-4o --[works_with]--> ChatGPT" in md_result.stdout

        no_json_directory = temp_path / "no-json"
        no_json_directory.mkdir()
        no_json = run_cli(
            [
                "analyze", "--text", "OpenAI created GPT-4o.",
                "--no-json",
            ],
            no_json_directory,
        )
        assert no_json.returncode == 0, no_json.stderr
        assert not (no_json_directory / "output.json").exists()
        assert (no_json_directory / "output.md").is_file()

        no_markdown_directory = temp_path / "no-markdown"
        no_markdown_directory.mkdir()
        no_markdown = run_cli(
            [
                "analyze", "--text", "OpenAI created GPT-4o.",
                "--no-markdown",
            ],
            no_markdown_directory,
        )
        assert no_markdown.returncode == 0, no_markdown.stderr
        assert (no_markdown_directory / "output.json").is_file()
        assert not (no_markdown_directory / "output.md").exists()

        no_results = run_cli(
            [
                "analyze", "--text", "plain lowercase words.",
                "--no-json", "--no-markdown",
            ],
            temp_path,
        )
        assert no_results.returncode == 0, no_results.stderr
        assert "Entities: 0" in no_results.stdout
        assert "Relationships: 0" in no_results.stdout
        assert (
            "No explicit supported relationships were detected."
            in no_results.stdout
        )

        missing = run_cli(
            ["analyze", str(temp_path / "missing.txt")], temp_path
        )
        assert missing.returncode != 0
        assert "does not exist" in missing.stderr
        assert "Traceback" not in missing.stderr

        unsupported_file = temp_path / "data.csv"
        unsupported_file.write_text("OpenAI created GPT-4o.", encoding="utf-8")
        unsupported = run_cli(["analyze", str(unsupported_file)], temp_path)
        assert unsupported.returncode != 0
        assert "Unsupported file extension" in unsupported.stderr

        empty_file = temp_path / "empty.txt"
        empty_file.write_text("   \n", encoding="utf-8")
        empty = run_cli(["analyze", str(empty_file)], temp_path)
        assert empty.returncode != 0
        assert "Input text is empty" in empty.stderr

        empty_text = run_cli(["analyze", "--text", ""], temp_path)
        assert empty_text.returncode != 0
        assert "Input text is empty" in empty_text.stderr

        both = run_cli(
            ["analyze", str(text_file), "--text", "OpenAI created GPT-4o."],
            temp_path,
        )
        assert both.returncode != 0
        assert "not allowed with argument" in both.stderr

        neither = run_cli(["analyze"], temp_path)
        assert neither.returncode != 0
        assert "required" in neither.stderr

        invalid_output = run_cli(
            [
                "analyze", "--text", "OpenAI created GPT-4o.",
                "--json", str(temp_path / "missing" / "result.json"),
                "--no-markdown",
            ],
            temp_path,
        )
        assert invalid_output.returncode != 0
        assert "Could not write output file" in invalid_output.stderr

        query_graph = temp_path / "query-graph.json"
        query_markdown = temp_path / "query-graph.md"
        query_analysis = run_cli(
            [
                "analyze",
                "--text",
                "Microsoft invested in OpenAI. OpenAI created GPT. "
                "GPT powers ChatGPT.",
                "--json",
                str(query_graph),
                "--markdown",
                str(query_markdown),
            ],
            temp_path,
        )
        assert query_analysis.returncode == 0, query_analysis.stderr

        path_result = run_cli(
            ["path", str(query_graph), "microsoft", "chatgpt"], temp_path
        )
        assert path_result.returncode == 0, path_result.stderr
        assert (
            "Microsoft --[invested_in]--> OpenAI --[created]--> GPT "
            "--[powers]--> ChatGPT" in path_result.stdout
        )

        undirected_result = run_cli(
            [
                "path", str(query_graph), "chatgpt", "microsoft",
                "--undirected",
            ],
            temp_path,
        )
        assert undirected_result.returncode == 0, undirected_result.stderr
        assert "ChatGPT <--[powers]-- GPT" in undirected_result.stdout

        neighbors_result = run_cli(
            [
                "neighbors", str(query_graph), "openai",
                "--direction", "both",
            ],
            temp_path,
        )
        assert neighbors_result.returncode == 0, neighbors_result.stderr
        assert "incoming: Microsoft --[invested_in]--> OpenAI" in (
            neighbors_result.stdout
        )
        assert "outgoing: OpenAI --[created]--> GPT" in neighbors_result.stdout

        stats_result = run_cli(["stats", str(query_graph)], temp_path)
        assert stats_result.returncode == 0, stats_result.stderr
        assert "Entities: 4" in stats_result.stdout
        assert "Relationships: 3" in stats_result.stdout
        assert "- powers: 1" in stats_result.stdout

        subgraph_json = temp_path / "selected-subgraph.json"
        subgraph_markdown = temp_path / "selected-subgraph.md"
        subgraph_result = run_cli(
            [
                "subgraph", str(query_graph), "openai", "--depth", "2",
                "--json", str(subgraph_json),
                "--markdown", str(subgraph_markdown),
            ],
            temp_path,
        )
        assert subgraph_result.returncode == 0, subgraph_result.stderr
        assert subgraph_json.is_file()
        assert subgraph_markdown.is_file()
        subgraph_data = json.loads(subgraph_json.read_text("utf-8"))
        assert len(subgraph_data["entities"]) == 4
        assert len(subgraph_data["relationships"]) == 3
        assert subgraph_data["relationships"][1]["evidence"] == (
            "OpenAI created GPT."
        )

        malformed_json = temp_path / "malformed.json"
        malformed_json.write_text('{"entities": []}', encoding="utf-8")
        malformed_result = run_cli(
            ["stats", str(malformed_json)], temp_path
        )
        assert malformed_result.returncode != 0
        assert "relationships" in malformed_result.stderr
        assert "Traceback" not in malformed_result.stderr

        missing_graph_result = run_cli(
            ["stats", str(temp_path / "missing-graph.json")], temp_path
        )
        assert missing_graph_result.returncode != 0
        assert "Could not read graph JSON" in missing_graph_result.stderr
        assert "Traceback" not in missing_graph_result.stderr

    print("CLI tests passed.")


if __name__ == "__main__":
    run_test()
