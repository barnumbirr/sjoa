# sjoa

`sjoa` is a powerful command-line tool designed to read metadata from torrent
files or magnet URIs. It provides a simple and efficient way to extract
information about torrents without the need to download the actual content.

> The Sjoa is a river in Innlandet county, Norway and is one of the best
> whitewater rafting rivers in Europe.
>
> <p style="font-size: 12px" align="right">
>     Source: <a href="https://en.wikipedia.org/wiki/Sjoa">Wikipedia</a>
> and <a href="https://www.oars.com/blog/best-whitewater-rafting-in-europe/">OARS</a>
> </p>

## Installation

`sjoa` is implemented in Python and can be installed using pip, the Python
package manager. To install `sjoa`, simply run:

```bash
$ pip install sjoa
```

## Usage

Once installed, you can use `sjoa` from the command line.

```
$ sjoa -t debian-12.0.0-amd64-DVD-1.iso.torrent
Name: debian-12.0.0-amd64-DVD-1.iso
Hash: b1680a55cfc8693c6c02de732dd17c33e251e8e5
Created: 2023-06-10 12:01:18 by mktorrent 1.1
Comment: "Debian CD from cdimage.debian.org"
Pieces:
  14996 of length 256 KiB
Tracker URLs:
  • http://bttracker.debian.org:6969/announce
Webseed URLs:
  • https://cdimage.debian.org/cdimage/release/12.0.0/amd64/iso-dvd/debian-12.0.0-amd64-DVD-1.iso
  • https://cdimage.debian.org/cdimage/archive/12.0.0/amd64/iso-dvd/debian-12.0.0-amd64-DVD-1.iso
Files: (3.66 GiB)
  • debian-12.0.0-amd64-DVD-1.iso, Size: 3.66 GiB
```

```
$ sjoa -m "magnet:?xt=urn:btih:2c6b6858d61da9543d4231a71db4b1c9264b0685&dn=ubuntu-22.04-desktop-amd64.iso&tr=https%3A%2F%2Ftorrent.ubuntu.com%2Fannounce&tr=https%3A%2F%2Fipv6.torrent.ubuntu.com%2Fannounce"
Name: ubuntu-22.04-desktop-amd64.iso
Hash: 2c6b6858d61da9543d4231a71db4b1c9264b0685
Tracker URLs:
  • https://torrent.ubuntu.com/announce
  • https://ipv6.torrent.ubuntu.com/announce
```

## License

```
Copyright 2023 Martin Simon

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
