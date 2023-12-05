#!/usr/bin/env python3

import sys
if sys.version_info >= (3, 8):
    from importlib import metadata
else:
    import importlib_metadata as metadata

def _get_version():
    try:
        version = metadata.version('sjoa')
    except:
        version = None
    return version

def _convert_bytes(size, decimals):
    units = ["bytes", "KiB", "MiB", "GiB", "TiB"]
    index = 0
    while size >= 1024 and index < len(units) - 1:
        size /= 1024
        index += 1
    return f"{size:.{decimals}f} {units[index]}"
