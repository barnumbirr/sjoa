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

def _display_data(data):
    optional_keys = ['name', 'hash', 'created', 'comment', 'pieces']
    for key in optional_keys:
        if key in data:
            print(f"{key.capitalize()}: {data[key]}")

    if 'trackers' in data:
        print("Tracker URLs:")
        for tracker in data.get('trackers', []):
            print(f"  • {tracker}")

    if 'webseeds' in data:
        print("Webseed URLs:")
        for webseed in data.get('webseeds', []):
            print(f"  • {webseed}")

    if 'files' in data:
        print(f"Files: ({data['total_torrent_size']})")
        for file in data.get('files', []):
            print(f"  • {file['path']}, Size: {file['size']}")
