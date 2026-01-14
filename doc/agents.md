# Claude code

## Development Environment

### Python Management (Backend)
**This project uses `uv` for Python package management.**

**CRITICAL**: Always prefix Python commands with `uv run`:
```bash
uv run python script.py
uv run uvicorn main:app
uv run pytest
uv run alembic upgrade head
```

**Package Management**:
```bash
uv sync                    # Install/sync all dependencies
uv add <package>           # Add a new package
uv pip install <package>   # Alternative package installation
```

**Never use**: `python`, `pip`, `venv` directly.
