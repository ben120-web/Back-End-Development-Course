# Contributing

1. Create a focused branch and describe the behaviour or security invariant
   being changed.
2. Install development dependencies with `python -m pip install -e ".[dev]"`.
3. Run `ruff check .`, `ruff format --check .` and `pytest -q`.
4. Add an adversarial regression test for every boundary or subprocess change.
5. Never commit API keys, `.env` files or sensitive fixture data.
