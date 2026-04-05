from __future__ import annotations

import pytest

from sjoa.decoder import _ps_magnet, _ps_torrent
from sjoa.models import CreationInfo, FileEntry, PieceInfo, TorrentMetadata


class TestPsTorrent:
    def test_returns_torrent_metadata(self, debian_torrent):
        result = _ps_torrent(debian_torrent)
        assert isinstance(result, TorrentMetadata)

    def test_hash(self, debian_torrent):
        result = _ps_torrent(debian_torrent)
        assert result.hash == "267d63ffd31770e467f8d985a86633f05502c10d"

    def test_name(self, debian_torrent):
        result = _ps_torrent(debian_torrent)
        assert result.name == "debian-12.2.0-amd64-DVD-1.iso"

    def test_size(self, debian_torrent):
        result = _ps_torrent(debian_torrent)
        assert result.size == 3994091520

    def test_creation(self, debian_torrent):
        result = _ps_torrent(debian_torrent)
        assert isinstance(result.creation, CreationInfo)
        assert result.creation.date is not None
        assert result.creation.tool is not None
        assert "mktorrent" in result.creation.tool

    def test_comment(self, debian_torrent):
        result = _ps_torrent(debian_torrent)
        assert result.comment == '"Debian CD from cdimage.debian.org"'

    def test_trackers(self, debian_torrent):
        result = _ps_torrent(debian_torrent)
        assert result.trackers is not None
        assert len(result.trackers) >= 1

    def test_webseeds(self, debian_torrent):
        result = _ps_torrent(debian_torrent)
        assert result.webseeds is not None
        assert len(result.webseeds) >= 1

    def test_single_file(self, debian_torrent):
        result = _ps_torrent(debian_torrent)
        assert len(result.files) == 1
        assert isinstance(result.files[0], FileEntry)
        assert result.files[0].path == "debian-12.2.0-amd64-DVD-1.iso"

    def test_pieces(self, debian_torrent):
        result = _ps_torrent(debian_torrent)
        assert isinstance(result.pieces, PieceInfo)
        assert result.pieces.total == 15237

    def test_all_expected_fields(self, debian_torrent):
        result = _ps_torrent(debian_torrent)
        assert result.hash is not None
        assert result.name is not None
        assert result.creation is not None
        assert result.comment is not None
        assert result.trackers is not None
        assert result.webseeds is not None
        assert len(result.files) >= 1
        assert result.size > 0
        assert result.pieces is not None

    def test_bbb_parses_successfully(self, bbb_torrent):
        result = _ps_torrent(bbb_torrent)
        assert result.name is not None
        assert result.hash is not None
        assert result.size > 0

    def test_bbb_has_files(self, bbb_torrent):
        result = _ps_torrent(bbb_torrent)
        assert len(result.files) >= 1

    def test_invalid_data_raises(self):
        with pytest.raises(Exception):  # noqa: B017
            _ps_torrent(b"not a torrent file")

    @pytest.mark.parametrize("private_val, expected", [(1, 1), (0, 0)])
    def test_private_flag(self, make_torrent, private_val, expected):
        data = make_torrent(extra_info={b"private": private_val})
        result = _ps_torrent(data)
        assert result.private == expected

    def test_private_absent_is_none(self, debian_torrent):
        result = _ps_torrent(debian_torrent)
        assert result.private is None

    @pytest.mark.parametrize(
        "field, accessor",
        [
            ("trackers", lambda r: r.trackers),
            ("webseeds", lambda r: r.webseeds),
            ("comment", lambda r: r.comment),
        ],
    )
    def test_missing_optional_field_is_none(self, make_torrent, field, accessor):
        result = _ps_torrent(make_torrent())
        assert accessor(result) is None

    def test_no_creation_info(self, make_torrent):
        result = _ps_torrent(make_torrent())
        assert result.creation is None

    def test_no_pieces(self, make_torrent):
        data = make_torrent(piece_length=0, pieces=b"")
        result = _ps_torrent(data)
        assert result.pieces is None

    def test_announce_without_announce_list(self, make_torrent):
        data = make_torrent(extra_top={b"announce": b"http://tracker.example.com/announce"})
        result = _ps_torrent(data)
        assert result.trackers == ["http://tracker.example.com/announce"]

    def test_non_utf8_name(self, make_torrent):
        data = make_torrent(name=b"\xff\xfetest")
        result = _ps_torrent(data)
        assert result.name is not None
        assert "test" in result.name

    def test_multi_file_torrent(self):
        import bencodepy

        data = bencodepy.encode(
            {
                b"info": {
                    b"name": b"my_album",
                    b"piece length": 262144,
                    b"pieces": b"\x00" * 20,
                    b"files": [
                        {b"length": 5000, b"path": [b"track01.mp3"]},
                        {b"length": 3000, b"path": [b"track02.mp3"]},
                        {b"length": 2000, b"path": [b"subdir", b"cover.jpg"]},
                    ],
                }
            }
        )
        result = _ps_torrent(data)
        assert len(result.files) == 3
        assert result.files[0].path == "track01.mp3"
        assert result.files[0].size == 5000
        assert result.files[1].size == 3000
        assert result.files[2].path == "subdir/cover.jpg"
        assert result.files[2].size == 2000
        assert result.size == 10000

    def test_size_is_raw_integer(self, debian_torrent):
        result = _ps_torrent(debian_torrent)
        assert isinstance(result.size, int)
        for f in result.files:
            assert isinstance(f.size, int)

    def test_pieces_are_raw_integers(self, debian_torrent):
        result = _ps_torrent(debian_torrent)
        assert isinstance(result.pieces.length, int)
        assert isinstance(result.pieces.last_piece_size, int)


class TestPsMagnet:
    SAMPLE_MAGNET = (
        "magnet:?xt=urn:btih:2c6b6858d61da9543d4231a71db4b1c9264b0685"
        "&dn=ubuntu-22.04-desktop-amd64.iso"
        "&tr=https%3A%2F%2Ftorrent.ubuntu.com%2Fannounce"
        "&tr=https%3A%2F%2Fipv6.torrent.ubuntu.com%2Fannounce"
    )

    def test_hash_extraction(self):
        result = _ps_magnet(self.SAMPLE_MAGNET)
        assert result["hash"] == "2c6b6858d61da9543d4231a71db4b1c9264b0685"

    def test_name_extraction(self):
        result = _ps_magnet(self.SAMPLE_MAGNET)
        assert result["name"] == "ubuntu-22.04-desktop-amd64.iso"

    def test_trackers_extraction(self):
        result = _ps_magnet(self.SAMPLE_MAGNET)
        assert isinstance(result["trackers"], list)
        assert len(result["trackers"]) == 2
        assert "https://torrent.ubuntu.com/announce" in result["trackers"]

    def test_minimal_magnet(self):
        result = _ps_magnet("magnet:?xt=urn:btih:abc123")
        assert result["hash"] == "abc123"

    def test_magnet_with_size(self):
        result = _ps_magnet("magnet:?xt=urn:btih:abc123&xl=1073741824")
        assert result["size"] == 1073741824

    def test_missing_fields_not_in_result(self):
        result = _ps_magnet("magnet:?xt=urn:btih:abc123")
        assert "name" not in result
        assert "trackers" not in result

    def test_empty_magnet(self):
        assert _ps_magnet("magnet:?") == {}

    def test_invalid_size_preserved(self):
        result = _ps_magnet("magnet:?xt=urn:btih:abc123&xl=notanumber")
        assert result["size"] == "notanumber"

    def test_size_is_raw_integer(self):
        result = _ps_magnet("magnet:?xt=urn:btih:abc123&xl=1073741824")
        assert isinstance(result["size"], int)

    def test_duplicate_trackers(self):
        magnet = (
            "magnet:?xt=urn:btih:abc123"
            "&tr=http%3A%2F%2Ftracker1.com"
            "&tr=http%3A%2F%2Ftracker2.com"
            "&tr=http%3A%2F%2Ftracker3.com"
        )
        result = _ps_magnet(magnet)
        assert isinstance(result["trackers"], list)
        assert len(result["trackers"]) == 3

    def test_unknown_params_preserved(self):
        result = _ps_magnet("magnet:?xt=urn:btih:abc123&custom_key=custom_value")
        assert result["custom_key"] == "custom_value"
