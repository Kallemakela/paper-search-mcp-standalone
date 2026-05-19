#!/usr/bin/env python3
"""CLI wrapper generated from the shared paper search API."""

from __future__ import annotations

import argparse
import asyncio
import inspect
import json
import sys
from typing import Any, get_args, get_origin

from .api import TOOLS


def _argument_type(annotation: Any) -> Any:
    if annotation is inspect._empty:
        return str
    origin = get_origin(annotation)
    if origin is None:
        return bool if annotation is bool else annotation
    args = [arg for arg in get_args(annotation) if arg is not type(None)]
    if len(args) == 1 and args[0] in (str, int, float, bool):
        return args[0]
    return str


def _add_argument(parser: argparse.ArgumentParser, name: str, parameter: inspect.Parameter) -> None:
    arg_type = _argument_type(parameter.annotation)
    if parameter.default is inspect._empty:
        parser.add_argument(name, type=arg_type)
        return
    option = f"--{name.replace('_', '-')}"
    if arg_type is bool:
        action = "store_false" if parameter.default else "store_true"
        parser.add_argument(option, action=action, default=parameter.default)
        return
    parser.add_argument(option, type=arg_type, default=parameter.default)


def add_cli_command_from_function(subparsers: Any, func: Any) -> None:
    """Create one CLI command from a shared API function."""
    doc = inspect.getdoc(func) or ""
    parser = subparsers.add_parser(
        func.__name__,
        help=doc.splitlines()[0] if doc else func.__name__,
        description=doc,
    )
    for name, parameter in inspect.signature(func).parameters.items():
        _add_argument(parser, name, parameter)
    parser.set_defaults(handler=func)


def build_parser() -> argparse.ArgumentParser:
    """Build the CLI from the shared API function list."""
    parser = argparse.ArgumentParser(prog="paper-search")
    subparsers = parser.add_subparsers(dest="command", required=True)
    for tool in TOOLS:
        add_cli_command_from_function(subparsers, tool)
    return parser


def _print_result(result: Any) -> None:
    if isinstance(result, str):
        print(result)
        return
    print(json.dumps(result, indent=2, default=str))


def main() -> None:
    """Run the CLI wrapper."""
    parser = build_parser()
    args = parser.parse_args()
    handler = args.handler
    kwargs = {key: value for key, value in vars(args).items() if key not in {"command", "handler"}}
    _print_result(asyncio.run(handler(**kwargs)))
    sys.exit(0)


if __name__ == "__main__":
    main()
