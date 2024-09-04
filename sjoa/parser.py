#!/usr/bin/env python3

import argparse
from .utils import _get_version

def _init_parser():
    parser = argparse.ArgumentParser(
        prog='sjoa',
        description='%(prog)s is a powerful command-line tool designed to read metadata from torrent files or magnet URIs.',
        epilog='Report bugs to https://github.com/barnumbirr/sjoa/issues',
        formatter_class=lambda prog: argparse.HelpFormatter(prog, width=80, max_help_position=40),
        add_help=False)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "-t",
        "--torrent",
        type=str,
        help='Path to torrent file.')
    group.add_argument(
        "-m",
        "--magnet",
        type=str,
        help='Magnet URI.')
    parser.add_argument(
        '-h',
        '--help',
        action='help',
        help='Show this help message and exit.')
    parser.add_argument(
        '-v',
        '--version',
        action='version',
        version=f'%(prog)s {_get_version()}',
        help='Show version information.')

    return parser

argparser = _init_parser()
