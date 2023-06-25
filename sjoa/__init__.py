#!/usr/bin/env python3

from .parser import argparser
from .decoder import _ps_torrent, _ps_magnet

def main():
    args = argparser.parse_args()

    if args.input_torrent.startswith('magnet:?'):
        return _ps_magnet(args.input_torrent)
    else:
        with open(args.input_torrent, 'rb') as file:
            return _ps_torrent(file.read())

if __name__ == "__main__":
    main()
