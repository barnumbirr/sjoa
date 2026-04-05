from __future__ import annotations

import dataclasses
import io

from rich.console import Console

from sjoa.display import _display_data
from sjoa.models import CreationInfo, FileEntry, PieceInfo, TorrentMetadata


def _capture_display(data: dict) -> str:
    buf = io.StringIO()
    console = Console(file=buf, force_terminal=False, width=120)
    _display_data(data, console=console)
    return buf.getvalue()


def _torrent_dict(**overrides) -> dict:
    """Build a display-ready dict from TorrentMetadata defaults."""
    defaults = TorrentMetadata(
        hash="abc123",
        name="test.iso",
        private=None,
        comment=None,
        trackers=None,
        webseeds=None,
        files=[FileEntry(path="test.iso", size=1073741824)],
        size=1073741824,
    )
    if overrides:
        defaults = dataclasses.replace(defaults, **overrides)
    return dataclasses.asdict(defaults)


class TestDisplayData:
    def test_minimal_data(self):
        output = _capture_display({"name": "test.iso", "hash": "abc123"})
        assert "test.iso" in output
        assert "abc123" in output

    def test_full_torrent_data(self):
        data = _torrent_dict(
            pieces=PieceInfo(total=100, length=262144, last_piece_size=65536),
            creation=CreationInfo(date="2023-10-07 12:03:00", tool="mktorrent 1.1"),
            comment="Test comment",
            private=1,
            trackers=["http://tracker1.com", "http://tracker2.com"],
            webseeds=["http://seed1.com"],
        )
        output = _capture_display(data)
        assert "test.iso" in output
        assert "1.00 GiB" in output
        assert "mktorrent 1.1" in output
        assert "Test comment" in output
        assert "True" in output
        assert "tracker1.com" in output
        assert "seed1.com" in output

    def test_creation_date_only(self):
        data = _torrent_dict(creation=CreationInfo(date="2023-10-07 12:03:00"))
        output = _capture_display(data)
        assert "2023-10-07 12:03:00" in output

    def test_creation_tool_only(self):
        data = _torrent_dict(creation=CreationInfo(tool="mktorrent 1.1"))
        output = _capture_display(data)
        assert "mktorrent 1.1" in output

    def test_magnet_data(self):
        data = {"name": "ubuntu.iso", "hash": "abc123", "trackers": ["http://tracker.com"]}
        output = _capture_display(data)
        assert "ubuntu.iso" in output
        assert "tracker.com" in output

    def test_empty_data(self):
        output = _capture_display({})
        assert output.strip() == ""

    def test_private_true(self):
        data = _torrent_dict(private=1)
        output = _capture_display(data)
        assert "True" in output

    def test_private_false(self):
        data = _torrent_dict(private=0)
        output = _capture_display(data)
        assert "False" in output

    def test_private_none_shows_false(self):
        data = _torrent_dict(private=None)
        output = _capture_display(data)
        assert "Private" in output
        assert "False" in output

    def test_multiple_files(self):
        data = _torrent_dict(
            files=[
                FileEntry(path="file1.txt", size=1024),
                FileEntry(path="file2.txt", size=2048),
                FileEntry(path="dir/file3.txt", size=3072),
            ]
        )
        output = _capture_display(data)
        assert "file1.txt" in output
        assert "file2.txt" in output
        assert "dir/file3.txt" in output
        assert "1.00 KiB" in output
        assert "2.00 KiB" in output
        assert "3.00 KiB" in output

    def test_none_values_skipped(self):
        data = {"name": "test.iso", "trackers": None, "webseeds": None}
        output = _capture_display(data)
        assert "test.iso" in output
        assert "Tracker" not in output
        assert "Webseed" not in output

    def test_size_formatted_from_integer(self):
        output = _capture_display({"size": 1073741824})
        assert "1.00 GiB" in output

    def test_pieces_formatted_from_integers(self):
        data = _torrent_dict(pieces=PieceInfo(total=50, length=262144, last_piece_size=131072))
        output = _capture_display(data)
        assert "50" in output
        assert "256 KiB" in output
        assert "128.00 KiB" in output

    def test_string_size_passthrough(self):
        output = _capture_display({"size": "1.00 GiB"})
        assert "1.00 GiB" in output
