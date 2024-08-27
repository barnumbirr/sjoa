<p align="center"><img src="./assets/sjoa.jpg" width=240></img></p>
<p align="center"><i>illustration generated using <a href="https://perchance.org/ai-pixel-art-generator">perchance.org</a></i></p>

<h1 align="center">sjoa</h1>

`sjoa` is a powerful command-line tool designed to read metadata from torrent
files or magnet URIs. It provides a simple and efficient way to extract
information about torrents without the need to download the actual content.

> The Sjoa is a river in Innlandet county, Norway and is one of the best
> whitewater rafting rivers in Europe renowned for its fast-moving, turbulent
> waters with Class II-V rapids depending on the water level.
>
> <p style="font-size: 12px" align="right">
>     Source: <a href="https://en.wikipedia.org/wiki/Sjoa">Wikipedia</a>
> and <a href="https://www.oars.com/blog/best-whitewater-rafting-in-europe/">OARS</a>
> </p>

The word `sjoa` was chosen as a play on words: the term "torrent" is often used
to describe a fast-flowing stream or river, typically characterized by strong
currents and rapid water movement.

## Installation

`sjoa` is implemented in Python and can be installed using pip, the Python
package manager. To install `sjoa`, simply run:

```bash
$ pip install sjoa
```

## Usage

Once installed, you can use `sjoa` from the command line.

```
$ sjoa -t examples/debian-12.2.0-amd64-DVD-1.iso.torrent
 Name            debian-12.2.0-amd64-DVD-1.iso
 Hash            267d63ffd31770e467f8d985a86633f05502c10d
 Size            3.72 GiB
 Pieces          15237 of length 256 KiB (last piece 64.00 KiB)
 Creation        2023-10-07 12:03:00 by mktorrent 1.1
 Comment         "Debian CD from cdimage.debian.org"
 Private         False
 Tracker URL(s)  • http://bttracker.debian.org:6969/announce
 Webseed URL(s)  • https://cdimage.debian.org/cdimage/release/12.2.0/amd64/iso-dvd/debian-12.2.0-amd64-DVD-1.iso
                 • https://cdimage.debian.org/cdimage/archive/12.2.0/amd64/iso-dvd/debian-12.2.0-amd64-DVD-1.iso
 Files           ┌───────────────────────────────────────────────────────────────────────┬─────────────────────┐
                 │ • debian-12.2.0-amd64-DVD-1.iso                                       │ 3.72 GiB            │
                 └───────────────────────────────────────────────────────────────────────┴─────────────────────┘
```

```
$ sjoa -m "magnet:?xt=urn:btih:2c6b6858d61da9543d4231a71db4b1c9264b0685&dn=ubuntu-22.04-desktop-amd64.iso&tr=https%3A%2F%2Ftorrent.ubuntu.com%2Fannounce&tr=https%3A%2F%2Fipv6.torrent.ubuntu.com%2Fannounce"
 Name            ubuntu-22.04-desktop-amd64.iso
 Hash            2c6b6858d61da9543d4231a71db4b1c9264b0685
 Tracker URL(s)  • https://torrent.ubuntu.com/announce
                 • https://ipv6.torrent.ubuntu.com/announce
```

## License

```
Copyright 2023-2024 Martin Simon

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
```

## Buy me a coffee?

If you feel like buying me a coffee (or a beer?), donations are welcome:

```
BTC : bc1qq04jnuqqavpccfptmddqjkg7cuspy3new4sxq9
DOGE: DRBkryyau5CMxpBzVmrBAjK6dVdMZSBsuS
ETH : 0x2238A11856428b72E80D70Be8666729497059d95
LTC : MQwXsBrArLRHQzwQZAjJPNrxGS1uNDDKX6
```
