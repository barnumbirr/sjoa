#!/usr/bin/env python3

import argparse
from .utils import _get_version

def _init_parser():
    parser = argparse.ArgumentParser(
        prog='sjoa',
        description='%(prog)s is a command-line tool to read metadata from torrent files or magnet URLs.',
        epilog='Report bugs to https://github.com/barnumbirr/sjoa/issues',
        add_help=False)
    parser.add_argument(
        'input_torrent',
        metavar='PATH / MAGNET_URL',
        type=str,
        help='Path to torrent file or magnet URL.')
    parser.add_argument(
        '-h',
        '--help',
        action='help',
        help='Show this help log.')
    parser.add_argument(
        '-v',
        '--version',
        action='version',
        version=f'%(prog)s {_get_version()}',
        help='Show version information.')

    return parser

argparser = _init_parser()
