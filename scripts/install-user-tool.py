#!/usr/bin/env python3
"""Install a pinned official release after verifying its published SHA256."""

import argparse
import hashlib
import io
from pathlib import Path
import platform
import subprocess
import tarfile
import urllib.request


def download(url):
    with urllib.request.urlopen(url, timeout=60) as response:
        return response.read()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('tool', choices=['chezmoi', 'starship', 'firacode'])
    args = parser.parse_args()
    arch = platform.machine()
    if platform.system() != 'Linux':
        parser.error('this installer supports Linux')
    if args.tool == 'chezmoi':
        mapping = {'x86_64': 'amd64', 'aarch64': 'arm64', 'armv7l': 'arm', 'armv6l': 'arm', 'i686': 'i386'}
        if arch not in mapping:
            parser.error('unsupported architecture; use the official chezmoi install documentation')
        version = '2.73.0'
        base = f'https://github.com/twpayne/chezmoi/releases/download/v{version}/'
        name = f'chezmoi_{version}_linux_{mapping[arch]}.tar.gz'
        checksum_file = f'chezmoi_{version}_checksums.txt'
    elif args.tool == 'starship':
        mapping = {'x86_64': 'x86_64', 'aarch64': 'aarch64', 'armv7l': 'arm', 'i686': 'i686'}
        if arch not in mapping:
            parser.error('unsupported architecture; use the official Starship install documentation')
        target = mapping[arch] + '-unknown-linux-' + ('musleabihf' if arch == 'armv7l' else 'musl')
        base = 'https://github.com/starship/starship/releases/download/v1.26.0/'
        name = f'starship-{target}.tar.gz'
        checksum_file = name + '.sha256'
    else:
        base = 'https://github.com/ryanoasis/nerd-fonts/releases/download/v3.5.1/'
        name = 'FiraCode.tar.xz'
        checksum_file = 'SHA-256.txt'
    checks = download(base + checksum_file).decode()
    candidates = [line.split()[0] for line in checks.splitlines() if line.split()[-1].lstrip('*') == name]
    if not candidates and args.tool == 'starship':
        candidates = [checks.split()[0]]
    if len(candidates) != 1:
        raise RuntimeError('expected one checksum for the requested release asset')
    data = download(base + name)
    if hashlib.sha256(data).hexdigest() != candidates[0]:
        raise RuntimeError('SHA256 mismatch; nothing has been installed')
    destination = Path.home() / ('.local/share/fonts/FiraCodeNerd' if args.tool == 'firacode' else '.local/bin')
    destination.mkdir(parents=True, exist_ok=True)
    count = 0
    with tarfile.open(fileobj=io.BytesIO(data)) as archive:
        for member in archive:
            basename = Path(member.name).name
            wanted = basename.endswith('.ttf') or basename in ['LICENSE', 'LICENSE.txt', 'OFL.txt'] if args.tool == 'firacode' else basename == args.tool
            if not member.isfile() or not wanted:
                continue
            target = destination / basename
            content = archive.extractfile(member).read()
            if target.exists() and target.read_bytes() == content:
                continue
            temporary = target.with_name(target.name + '.pumuarch-new')
            temporary.write_bytes(content)
            temporary.chmod(0o644 if args.tool == 'firacode' else 0o755)
            temporary.replace(target)
            count += 1
    if args.tool == 'firacode':
        subprocess.run(['fc-cache', '-f', str(destination)], check=True)
    print(f'Verified {name}; installed or updated {count} files in {destination}')


if __name__ == '__main__':
    main()
