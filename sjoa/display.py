from __future__ import annotations

from collections.abc import Callable
from typing import Any

from rich.console import Console
from rich.table import Table

from .utils import _convert_bytes

_DISPLAY_ORDER = (
    "name",
    "hash",
    "size",
    "pieces",
    "creation",
    "comment",
    "private",
    "trackers",
    "webseeds",
    "files",
)

_KEY_LABELS: dict[str, str] = {"trackers": "Tracker URL(s)", "webseeds": "Webseed URL(s)"}


def _format_creation(value: dict[str, str]) -> str:
    parts = []
    if value.get("date"):
        parts.append(value["date"])
    if value.get("tool"):
        parts.append(f"by {value['tool']}")
    return " ".join(parts)


def _format_pieces(value: dict[str, Any]) -> str:
    length = value["length"]
    if isinstance(length, (int, float)):
        length = _convert_bytes(length, 0)
    last = value["last_piece_size"]
    if isinstance(last, (int, float)):
        last = _convert_bytes(last, 2)
    return f"{value['total']} of length {length} (last piece {last})"


def _format_private(value: int | None) -> str:
    return "True" if value == 1 else "False"


_VALUE_FORMATTERS: dict[str, Callable[[Any], str]] = {
    "creation": _format_creation,
    "pieces": _format_pieces,
    "private": _format_private,
}


def _render_files(table: Table, label: str, files: list[dict[str, Any]]) -> None:
    sub_table = Table(show_header=False, expand=True)
    sub_table.add_column("File Path")
    sub_table.add_column("File Size")

    for file_data in files:
        file_size = file_data["size"]
        if isinstance(file_size, (int, float)):
            file_size = _convert_bytes(file_size, 2)
        sub_table.add_row(f"• {file_data['path']}", str(file_size))

    table.add_row(f"[bold]{label}[/bold]", sub_table)


def _display_data(data: dict[str, Any], console: Console | None = None) -> None:
    if console is None:
        console = Console()

    main_table = Table(show_header=False, box=None)

    for key in _DISPLAY_ORDER:
        if key not in data or (data[key] is None and key != "private"):
            continue

        label = _KEY_LABELS.get(key, key.capitalize())
        value = data[key]

        if key == "files":
            _render_files(main_table, label, value)
        else:
            formatter = _VALUE_FORMATTERS.get(key)
            if formatter:
                value = formatter(value)
            elif key == "size" and isinstance(value, (int, float)):
                value = _convert_bytes(value, 2)
            elif isinstance(value, list):
                value = "\n".join(f"• {v}" for v in value)
            elif isinstance(value, dict):
                value = "\n".join(f"{k}: {v}" for k, v in value.items())

            main_table.add_row(f"[bold]{label}[/bold]", str(value))

    console.print(main_table)
