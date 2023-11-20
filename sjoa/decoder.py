#!/usr/bin/env python3

import hashlib
import datetime
import bencodepy
import urllib.parse
from .utils import _convert_bytes

def _ps_torrent(file):
    metadata = {}
    decoded_data = bencodepy.decode(file)

    _hash = decoded_data.get(b'info', {})
    if _hash:
        metadata['hash'] = hashlib.sha1(bencodepy.encode(_hash)).hexdigest()

    name = decoded_data.get(b'info', {}).get(b'name')
    if name:
        metadata['name'] = name.decode()

    creation_date = decoded_data.get(b'creation date')
    created_by = decoded_data.get(b'created by').decode()
    if creation_date:
        creation_datetime = datetime.datetime.utcfromtimestamp(creation_date)
        metadata['created'] = creation_datetime.isoformat(' ')
    if created_by:
        metadata['created'] += f" by {created_by}"

    comment = decoded_data.get(b'comment')
    if comment:
        metadata['comment'] = comment.decode()

    announce_list = decoded_data.get(b'announce-list')
    if announce_list:
        metadata['trackers'] = [tracker[0].decode() for tracker in announce_list]
    else:
        announce = decoded_data.get(b'announce')
        if announce:
            metadata['trackers'] = [announce.decode()]

    webseeds = decoded_data.get(b'url-list')
    if webseeds:
        metadata['webseeds'] = [webseed.decode() for webseed in webseeds]

    file_list = []
    total_torrent_size = 0
    files = decoded_data.get(b'info', {}).get(b'files')
    if files:
        for file in files:
            file_path = b'/'.join(file.get(b'path', [])).decode()
            file_size = file.get(b'length')
            file_list.append({
                'path': file_path,
                'size': _convert_bytes(file_size, 2)
            })
            total_torrent_size += file_size
    else:
        single_file_name = decoded_data.get(b'info', {}).get(b'name', b'').decode()
        single_file_size = decoded_data.get(b'info', {}).get(b'length', 0)
        file_list.append({
            'path': single_file_name,
            'size': _convert_bytes(single_file_size, 2)
        })
        total_torrent_size = single_file_size

    metadata['files'] = file_list
    metadata['total_torrent_size'] = _convert_bytes(total_torrent_size, 2)

    piece_length = decoded_data.get(b'info', {}).get(b'piece length')
    pieces = decoded_data.get(b'info', {}).get(b'pieces')
    if piece_length and pieces:
       piece_length_size = _convert_bytes(piece_length, 0)
       num_pieces = len(pieces) // 20
       last_piece_size = total_torrent_size - (num_pieces - 1) * piece_length
       last_piece_size = _convert_bytes(last_piece_size, 2)
       metadata['pieces'] = f"\n  {num_pieces} of length {piece_length_size} (last piece {last_piece_size})"

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
