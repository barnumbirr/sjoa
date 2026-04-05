from __future__ import annotations

import json
import os

from tests.conftest import EXAMPLES_DIR, run_cli

DEBIAN_TORRENT = os.path.join(EXAMPLES_DIR, "debian-12.2.0-amd64-DVD-1.iso.torrent")
SAMPLE_MAGNET = (
    "magnet:?xt=urn:btih:2c6b6858d61da9543d4231a71db4b1c9264b0685"
    "&dn=ubuntu-22.04-desktop-amd64.iso"
    "&tr=https%3A%2F%2Ftorrent.ubuntu.com%2Fannounce"
)


class TestMainTorrentFile:
    def test_returns_zero(self):
        code, _, _ = run_cli("-t", DEBIAN_TORRENT)
        assert code == 0

    def test_produces_output(self):
        _, out, _ = run_cli("-t", DEBIAN_TORRENT)
        assert "debian-12.2.0-amd64-DVD-1.iso" in out

    def test_json_output(self):
        code, out, _ = run_cli("-t", DEBIAN_TORRENT, "-j")
        assert code == 0
        data = json.loads(out)
        assert data["name"] == "debian-12.2.0-amd64-DVD-1.iso"
        assert isinstance(data["size"], int)

    def test_json_has_raw_integers(self):
        _, out, _ = run_cli("-t", DEBIAN_TORRENT, "-j")
        data = json.loads(out)
        assert isinstance(data["size"], int)
        assert isinstance(data["files"][0]["size"], int)
        assert isinstance(data["pieces"]["length"], int)
        assert isinstance(data["pieces"]["last_piece_size"], int)


class TestMainMagnet:
    def test_returns_zero(self):
        code, _, _ = run_cli("-m", SAMPLE_MAGNET)
        assert code == 0

    def test_produces_output(self):
        _, out, _ = run_cli("-m", SAMPLE_MAGNET)
        assert "ubuntu-22.04-desktop-amd64.iso" in out

    def test_json_output(self):
        code, out, _ = run_cli("-m", SAMPLE_MAGNET, "-j")
        assert code == 0
        data = json.loads(out)
        assert data["name"] == "ubuntu-22.04-desktop-amd64.iso"
        assert data["hash"] == "2c6b6858d61da9543d4231a71db4b1c9264b0685"


class TestMainStdin:
    def test_torrent_from_stdin(self):
        with open(DEBIAN_TORRENT, "rb") as f:
            torrent_bytes = f.read()
        code, _, _ = run_cli("-t", "-", stdin_data=torrent_bytes)
        assert code == 0

    def test_magnet_from_stdin(self):
        code, out, _ = run_cli("-m", "-", stdin_data=SAMPLE_MAGNET)
        assert code == 0
        assert "ubuntu-22.04-desktop-amd64.iso" in out


class TestMainErrors:
    def test_file_not_found(self):
        code, _, err = run_cli("-t", "/nonexistent/file.torrent")
        assert code == 1
        assert "file not found" in err

    def test_invalid_torrent_data(self):
        code, _, err = run_cli("-t", "-", stdin_data=b"not a torrent file")
        assert code == 1
        assert "Error" in err

    def test_generic_exception(self):
        from unittest.mock import patch

        with patch("sjoa._ps_magnet", side_effect=RuntimeError("unexpected")):
            code, _, err = run_cli("-m", "magnet:?xt=urn:btih:abc")
        assert code == 1
        assert "unexpected" in err
