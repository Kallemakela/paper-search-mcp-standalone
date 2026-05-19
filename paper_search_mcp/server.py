"""Compatibility wrapper for the shared API and MCP entrypoint."""

from . import api as _api
from .mcp import main, mcp

globals().update(
    {
        name: value
        for name, value in _api.__dict__.items()
        if not (name.startswith("__") and name.endswith("__"))
    }
)


if __name__ == "__main__":
    main()
