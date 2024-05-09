#!/usr/bin/env python3

import hashlib
import datetime
import bencodepy
import urllib.parse
from .utils import _convert_bytes

def _ps_torrent(file):
    metadata = {}
    decoded_data = bencodepy.decode(file)
    info = decoded_data.get(b'info', {})

    metadata['hash'] = hashlib.sha1(bencodepy.encode(info)).hexdigest() if info else None
    metadata['name'] = info.get(b'name').decode() if info.get(b'name') else None
    metadata['private'] = info.get(b'private') if info.get(b'private') else None

    creation = {}
    creation['date'] = datetime.datetime.utcfromtimestamp(
        decoded_data.get(b"creation date")
    ).isoformat(' ')
    creation['tool'] = decoded_data.get(b'created by').decode()
    metadata['creation'] = creation

    metadata['comment'] = decoded_data.get(b'comment') and decoded_data.get(b'comment').decode()

    announce_list = decoded_data.get(b'announce-list')
    announce = decoded_data.get(b'announce')
    metadata['trackers'] = [tracker[0].decode() for tracker in announce_list] if announce_list else [announce.decode()] if announce else None

    webseeds = decoded_data.get(b'url-list')
    metadata['webseeds'] = [webseed.decode() for webseed in webseeds] if webseeds else None

    file_list = []
    total_torrent_size = 0
    files = info.get(b'files')
    if files:
        for file_info in files:
            file_path = b'/'.join(file_info.get(b'path', [])).decode()
            file_size = file_info.get(b'length')
            file_list.append({'path': file_path, 'size': _convert_bytes(file_size, 2)})
            total_torrent_size += file_size
    else:
        single_file_name = info.get(b'name', b'').decode()
        single_file_size = info.get(b'length', 0)
        file_list.append({'path': single_file_name, 'size': _convert_bytes(single_file_size, 2)})
        total_torrent_size = single_file_size
    metadata['files'] = file_list
    metadata['size'] = _convert_bytes(total_torrent_size, 2)

    piece_length = info.get(b'piece length')
    pieces = info.get(b'pieces')
    if piece_length and pieces:
        piece_length_size = _convert_bytes(piece_length, 0)
        num_pieces = len(pieces) // 20
        last_piece_size = total_torrent_size - (num_pieces - 1) * piece_length
        last_piece_size = _convert_bytes(last_piece_size, 2)
        metadata['pieces'] = {
            'total': num_pieces,
            'length': piece_length_size,
            'last_piece_size': last_piece_size
        }

    return metadata

def _ps_magnet(link):
    metadata = {}
    ps_magnet_url = urllib.parse.urlparse(link)
    query_params = urllib.parse.parse_qs(ps_magnet_url.query)

    key_mapping = {
        'xt': 'hash',
        'dn': 'name',
        'xl': 'size',
        'tr': 'trackers',
        'ws': 'webseeds',
        'as': 'acceptable_sources',
        'xs': 'exact_sources',
        'kt': 'keywords',
        'mt': 'manifests',
        'so': 'selects',
        'x.pe': 'peers'
    }

    for key, values in query_params.items():
        decoded_values = [urllib.parse.unquote(value) for value in values]
        if len(decoded_values) == 1:
            decoded_values = decoded_values[0]
        mapped_key = key_mapping.get(key, key)
        if mapped_key == 'hash' and isinstance(decoded_values, str) and decoded_values.startswith('urn:btih:'):
            decoded_values = decoded_values[len('urn:btih:'):]
        if mapped_key == 'size':
            decoded_values = _convert_bytes(int(decoded_values), 2)

        metadata[mapped_key] = decoded_values

    return metadata
