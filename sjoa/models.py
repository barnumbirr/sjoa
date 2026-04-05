from __future__ import annotations

from dataclasses import dataclass


@dataclass
class FileEntry:
    path: str
    size: int


@dataclass
class CreationInfo:
    date: str | None = None
    tool: str | None = None


@dataclass
class PieceInfo:
    total: int
    length: int
    last_piece_size: int


@dataclass
class TorrentMetadata:
    hash: str | None
    name: str | None
    private: int | None
    comment: str | None
    trackers: list[str] | None
    webseeds: list[str] | None
    files: list[FileEntry]
    size: int
    creation: CreationInfo | None = None
    pieces: PieceInfo | None = None
