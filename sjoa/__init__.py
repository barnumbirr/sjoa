from __future__ import annotations

__version__ = "1.4.0"

import dataclasses
import json
import sys

import bencodepy

from .decoder import _ps_magnet, _ps_torrent
from .display import _display_data
from .models import TorrentMetadata
from .parser import argparser


def main() -> int:
    args = argparser.parse_args()

    try:
        if args.magnet:
            magnet_input = sys.stdin.read().strip() if args.magnet == "-" else args.magnet
            data = _ps_magnet(magnet_input)
        elif args.torrent:
            if args.torrent == "-":
                file_data = sys.stdin.buffer.read()
            else:
                with open(args.torrent, "rb") as file:
                    file_data = file.read()
            data = _ps_torrent(file_data)
    except FileNotFoundError:
        print(f"Error: file not found: {args.torrent}", file=sys.stderr)
        return 1
    except bencodepy.DecodingError:
        print("Error: invalid or corrupt torrent file", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    if isinstance(data, TorrentMetadata):
        data = dataclasses.asdict(data)

    if args.json:
        print(json.dumps(data, indent=2))
    else:
        _display_data(data)

    return 0
