# Workspace-Bounded Coding Agent

[![CI](https://github.com/ben120-web/Back-End-Development-Course/actions/workflows/ci.yml/badge.svg)](https://github.com/ben120-web/Back-End-Development-Course/actions/workflows/ci.yml)

A compact tool-using coding agent built with the Google Gen AI SDK. The model
can inspect, edit and execute Python inside an explicitly selected workspace;
all filesystem tools resolve real paths and reject traversal and symlink escapes.
Child processes receive an allowlisted environment and a fixed timeout; stdout
and stderr returned to the model are truncated to a documented limit.

This began as a Boot.dev backend exercise and has been retained as a focused
example of agent orchestration and tool-boundary design.

Every change is linted, format-checked, tested and built as an installable
package. The `v1.0.0` tag publishes the verified wheel and source archive on a
GitHub release; it does not publish to PyPI.

## Version 1.0.0

The first stable portfolio release provides an installable `workspace-agent`
CLI, configurable model selection, real-path filesystem boundaries, a scrubbed
child-process environment, output limits, timeouts, adversarial boundary tests,
CodeQL, dependency review, Dependabot and tag-gated delivery. Six unit tests,
Ruff checks, package construction and an installed-CLI smoke test form the
release gate.

## Run

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
export GEMINI_API_KEY="..."

workspace-agent --workspace ./calculator "fix the calculator tests"
```

Use `--verbose` to print tool calls and token usage. The agent is limited to 20
model turns and Python subprocesses time out after 30 seconds. It defaults to
Google's stable
[`gemini-3.5-flash`](https://ai.google.dev/gemini-api/docs/models/gemini-3.5-flash);
use `--model` or `GEMINI_MODEL` to select a different model.

## Security model

- Every requested path is resolved before access.
- Traversal and symlinks outside the selected workspace are rejected.
- Only `.py` files may be executed.
- Child processes do not inherit API credentials; returned stdout and stderr
  are truncated.
- The API key is read from the environment and must never be committed.

The filesystem boundary is a defence against accidental path escape, not a
host-security sandbox. Executed Python still has the current user's operating
system and network permissions. Run it only against disposable workspaces; use
a locked-down container or microVM before accepting untrusted code.

## Architecture

```text
user task → model → typed tool request → boundary validation → filesystem/process
                 ↑                                      ↓
                 └──────── structured tool result ──────┘
```

The model never receives an unrestricted shell tool. Reads, writes, listings
and Python execution pass through one shared real-path boundary check. This
reduces authority and keeps the security policy testable in ordinary unit tests.

## Test

```bash
pytest -q
ruff check .
```
