from __future__ import annotations

_BYTE_UNITS = ("bytes", "KiB", "MiB", "GiB", "TiB")


def _convert_bytes(size: int | float, decimals: int) -> str:
    for unit in _BYTE_UNITS:
        if size < 1024 or unit == _BYTE_UNITS[-1]:
            return f"{size:.{decimals}f} {unit}"
        size /= 1024
    return ""  # unreachable, satisfies type checker
