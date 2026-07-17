# Sandboxed Coding Agent

A compact tool-using coding agent built with the Google Gen AI SDK. The model
can inspect, edit and execute Python inside an explicitly selected workspace;
all filesystem tools resolve real paths and reject traversal and symlink escapes.

This began as a Boot.dev backend exercise and has been retained as a focused
example of agent orchestration and tool-boundary design.

## Run

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
export GEMINI_API_KEY="..."

python main.py --workspace ./calculator "fix the calculator tests"
```

Use `--verbose` to print tool calls and token usage. The agent is limited to 20
model turns and Python subprocesses time out after 30 seconds.

## Security model

- Every requested path is resolved before access.
- Traversal and symlinks outside the selected workspace are rejected.
- Only `.py` files may be executed.
- Subprocess output is captured and execution has a timeout.
- The API key is read from the environment and must never be committed.

This is still an educational sandbox, not an isolation boundary for hostile
code. Run it only against disposable workspaces and never against sensitive
directories.

## Test

```bash
pytest -q
ruff check .
```
