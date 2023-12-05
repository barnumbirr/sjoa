#!/usr/bin/env python3

from .parser import argparser
from .display import _display_data
from .decoder import _ps_torrent, _ps_magnet

def main():
    args = argparser.parse_args()

    if args.magnet:
        return _display_data(_ps_magnet(args.magnet))
    elif args.torrent:
        try:
            with open(args.torrent, 'rb') as file:
                return _display_data(_ps_torrent(file.read()))
        except Exception as e:
            return f"Error: {e}"

if __name__ == "__main__":
    main()
