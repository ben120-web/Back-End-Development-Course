from pathlib import Path

from functions.get_file_content import get_file_content
from functions.get_files_info import get_files_info
from functions.run_python_file import run_python_file
from functions.write_file import write_file


def test_read_write_and_listing(tmp_path: Path) -> None:
    assert write_file(str(tmp_path), "nested/example.txt", "hello").startswith("Successfully")
    assert get_file_content(str(tmp_path), "nested/example.txt") == "hello"
    assert "example.txt" in get_files_info(str(tmp_path), "nested")


def test_path_traversal_is_rejected(tmp_path: Path) -> None:
    assert get_file_content(str(tmp_path), "../secret.txt").startswith("Error:")
    assert write_file(str(tmp_path), "/tmp/escaped.txt", "no").startswith("Error:")


def test_symlink_escape_is_rejected(tmp_path: Path) -> None:
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    outside = tmp_path / "outside-agent-test.txt"
    outside.write_text("secret", encoding="utf-8")
    (workspace / "link.txt").symlink_to(outside)
    assert get_file_content(str(workspace), "link.txt").startswith("Error:")


def test_python_execution_is_bounded(tmp_path: Path) -> None:
    script = tmp_path / "hello.py"
    script.write_text("print('hello')\n", encoding="utf-8")
    result = run_python_file(str(tmp_path), "hello.py")
    assert "EXIT_CODE: 0" in result
    assert "STDOUT: hello" in result


def test_python_execution_does_not_inherit_api_credentials(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("GEMINI_API_KEY", "must-not-reach-child")
    script = tmp_path / "environment.py"
    script.write_text(
        "import os\nprint(os.environ.get('GEMINI_API_KEY', 'not-set'))\n",
        encoding="utf-8",
    )

    result = run_python_file(str(tmp_path), "environment.py")

    assert "must-not-reach-child" not in result
    assert "STDOUT: not-set" in result


def test_python_output_is_truncated(tmp_path: Path) -> None:
    script = tmp_path / "noisy.py"
    script.write_text("print('x' * 12000)\n", encoding="utf-8")

    result = run_python_file(str(tmp_path), "noisy.py")

    assert "[truncated" in result
    assert len(result) < 10200
