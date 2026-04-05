# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/),
and this project adheres to [Semantic Versioning](https://semver.org/).

## [1.4.0] - 2026-04-05

### Fixed

- Fix `private=0` being silently converted to `None` instead of preserving the value
- Fix empty torrent comment returning raw bytes instead of `None`
- Fix crash on magnet links with non-numeric size values
- Fix crash on torrent files containing non-UTF-8 encoded strings

### Changed

- Decoder now returns raw integers for all size fields; formatting moved to display layer
- JSON output now contains machine-parseable integer byte counts instead of pre-formatted strings
- Error messages are now specific to the failure type (file not found, corrupt torrent, etc.)
- Display layer skips `None` values instead of rendering them
- Torrent decoder returns `TorrentMetadata` dataclass instead of plain dict
- Introduce `FileEntry`, `CreationInfo`, `PieceInfo` dataclasses for structured metadata
- Add type hints to all functions across all modules
- Extract display formatters into dispatch-based architecture
- Centralize byte decoding in `_decode_bytes()` helper
- Refactor `_convert_bytes()` to data-driven for/break pattern
- Use list comprehension + `sum()` for file list construction
- Remove `_get_version()` indirection; import `__version__` directly
- Remove shebangs from library modules

### Added

- `sjoa/models.py` with `TorrentMetadata`, `FileEntry`, `CreationInfo`, `PieceInfo` dataclasses
- `tests/conftest.py` with `make_torrent` factory fixture and `run_cli` test helper
- Integration tests for CLI entry point (`main()`)
- Display output assertions (previously smoke tests only)
- Multi-file torrent test coverage
- Edge case tests for decoder (private flag, no trackers, non-UTF-8, invalid magnet sizes)
- `@pytest.mark.parametrize` for related test cases
- CI workflow is now reusable via `workflow_call`
- Explicit permissions blocks on all CI/CD workflow jobs

## [1.3.1] - 2024-09-04

### Changed

- Set display width to 80 characters

## [1.3.0] - 2024-05-09

### Added

- Handle private torrent files
- Add Big Buck Bunny example torrent file

### Changed

- Update `rich` dependency

## [1.2.0] - 2023-12-05

### Changed

- Improve `_ps_torrent()` parsing
- Use `rich` for displaying data
- Better error handling
- Clean up metadata dict

## [1.1.0] - 2023-10-13

### Added

- Separate torrent (`-t`) and magnet (`-m`) handling

### Fixed

- Fix calculation of last piece size

## [1.0.0] - 2023-06-25

### Added

- Initial release
- Parse torrent files and magnet URIs
- Display metadata in terminal or as JSON
