from __future__ import annotations

import argparse

from . import __version__


def _init_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="sjoa",
        description=(
            "%(prog)s is a powerful command-line tool designed to read metadata from torrent files or magnet URIs."
        ),
        epilog="Report bugs to https://github.com/barnumbirr/sjoa/issues",
        formatter_class=lambda prog: argparse.HelpFormatter(prog, width=80, max_help_position=40),
        add_help=False,
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-t", "--torrent", type=str, help='Path to torrent file (use "-" for stdin).')
    group.add_argument("-m", "--magnet", type=str, help='Magnet URI (use "-" for stdin).')
    parser.add_argument("-j", "--json", action="store_true", default=False, help="Output metadata as JSON.")
    parser.add_argument("-h", "--help", action="help", help="Show this help message and exit.")
    parser.add_argument(
        "-v", "--version", action="version", version=f"%(prog)s {__version__}", help="Show version information."
    )

    return parser


argparser = _init_parser()
