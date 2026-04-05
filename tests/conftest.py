from __future__ import annotations

import io
import os
from contextlib import ExitStack, redirect_stderr, redirect_stdout
from unittest.mock import patch

import bencodepy
import pytest

from sjoa import main

EXAMPLES_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "examples")


@pytest.fixture
def debian_torrent() -> bytes:
    path = os.path.join(EXAMPLES_DIR, "debian-12.2.0-amd64-DVD-1.iso.torrent")
    with open(path, "rb") as f:
        return f.read()


@pytest.fixture
def bbb_torrent() -> bytes:
    path = os.path.join(EXAMPLES_DIR, "bbb_sunflower_1080p_60fps_normal.mp4.torrent")
    with open(path, "rb") as f:
        return f.read()


@pytest.fixture
def make_torrent():
    """Factory fixture for creating synthetic bencoded torrent data."""

    def _make(
        *,
        name: bytes = b"test.iso",
        length: int = 1024,
        piece_length: int = 512,
        pieces: bytes = b"",
        extra_info: dict | None = None,
        extra_top: dict | None = None,
    ) -> bytes:
        info: dict = {b"name": name, b"length": length, b"piece length": piece_length, b"pieces": pieces}
        if extra_info:
            info.update(extra_info)
        top: dict = {b"info": info}
        if extra_top:
            top.update(extra_top)
        return bencodepy.encode(top)

    return _make


class _FakeStdin:
    """Minimal stdin mock with a .buffer attribute for binary reads."""

    def __init__(self, data: bytes) -> None:
        self.buffer = io.BytesIO(data)


def run_cli(*args: str, stdin_data: bytes | str | None = None) -> tuple[int, str, str]:
    """Run sjoa CLI with given args, returning (exit_code, stdout, stderr)."""
    out, err = io.StringIO(), io.StringIO()
    with ExitStack() as stack:
        stack.enter_context(patch("sys.argv", ["sjoa", *args]))
        if stdin_data is not None:
            stdin_mock = _FakeStdin(stdin_data) if isinstance(stdin_data, bytes) else io.StringIO(stdin_data)
            stack.enter_context(patch("sys.stdin", stdin_mock))
        stack.enter_context(redirect_stdout(out))
        stack.enter_context(redirect_stderr(err))
        code = main()
    return code, out.getvalue(), err.getvalue()
