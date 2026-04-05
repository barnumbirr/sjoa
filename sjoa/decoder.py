from __future__ import annotations

import datetime
import hashlib
import urllib.parse
from typing import Any

import bencodepy

from .models import CreationInfo, FileEntry, PieceInfo, TorrentMetadata

_SHA1_HASH_SIZE = 20


def _decode_bytes(data: bytes | None) -> str | None:
    """Decode bencode bytes to str, replacing invalid characters."""
    return data.decode(errors="replace") if data else None


def _ps_torrent(data: bytes) -> TorrentMetadata:
    decoded_data = bencodepy.decode(data)
    info = decoded_data.get(b"info", {})

    info_hash = hashlib.sha1(bencodepy.encode(info)).hexdigest() if info else None
    name = _decode_bytes(info.get(b"name"))
    private = info.get(b"private")

    creation_date = decoded_data.get(b"creation date")
    created_by = decoded_data.get(b"created by")
    creation = None
    if creation_date is not None or created_by is not None:
        creation = CreationInfo(
            date=(
                datetime.datetime.fromtimestamp(creation_date, tz=datetime.timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
                if creation_date is not None
                else None
            ),
            tool=_decode_bytes(created_by),
        )

    comment = _decode_bytes(decoded_data.get(b"comment"))

    announce_list = decoded_data.get(b"announce-list")
    announce = decoded_data.get(b"announce")
    if announce_list:
        trackers = [tracker[0].decode(errors="replace") for tracker in announce_list]
    elif announce:
        trackers = [announce.decode(errors="replace")]
    else:
        trackers = None

    webseeds_raw = decoded_data.get(b"url-list")
    webseeds = [ws.decode(errors="replace") for ws in webseeds_raw] if webseeds_raw else None

    raw_files = info.get(b"files")
    if raw_files:
        files = [
            FileEntry(
                path=_decode_bytes(b"/".join(f.get(b"path", []))) or "",
                size=f.get(b"length", 0),
            )
            for f in raw_files
        ]
    else:
        files = [FileEntry(path=_decode_bytes(info.get(b"name", b"")) or "", size=info.get(b"length", 0))]
    total_size = sum(f.size for f in files)

    piece_length = info.get(b"piece length")
    raw_pieces = info.get(b"pieces")
    pieces = None
    if piece_length and raw_pieces:
        num_pieces = len(raw_pieces) // _SHA1_HASH_SIZE
        pieces = PieceInfo(
            total=num_pieces,
            length=piece_length,
            last_piece_size=total_size - (num_pieces - 1) * piece_length,
        )

    return TorrentMetadata(
        hash=info_hash,
        name=name,
        private=private if private is not None else None,
        comment=comment,
        trackers=trackers,
        webseeds=webseeds,
        files=files,
        size=total_size,
        creation=creation,
        pieces=pieces,
    )


def _ps_magnet(link: str) -> dict[str, Any]:
    metadata: dict[str, Any] = {}
    parsed_url = urllib.parse.urlparse(link)
    query_params = urllib.parse.parse_qs(parsed_url.query)

    key_mapping = {
        "xt": "hash",
        "dn": "name",
        "xl": "size",
        "tr": "trackers",
        "ws": "webseeds",
        "as": "acceptable_sources",
        "xs": "exact_sources",
        "kt": "keywords",
        "mt": "manifests",
        "so": "selects",
        "x.pe": "peers",
    }

    for key, values in query_params.items():
        decoded_values: Any = [urllib.parse.unquote(value) for value in values]
        if len(decoded_values) == 1:
            decoded_values = decoded_values[0]
        mapped_key = key_mapping.get(key, key)
        if mapped_key == "hash" and isinstance(decoded_values, str) and decoded_values.startswith("urn:btih:"):
            decoded_values = decoded_values[len("urn:btih:") :]
        if mapped_key == "size":
            try:  # noqa: SIM105
                decoded_values = int(decoded_values)
            except (ValueError, TypeError):
                pass

        metadata[mapped_key] = decoded_values

    return metadata
