#!/usr/bin/env python3
"""Check profile dependencies; install packages only with --install."""

import argparse
import importlib.util
import json
import os
from pathlib import Path
import re
import shlex
import shutil
import subprocess
import sys

REPO = Path(__file__).resolve().parent.parent


def distribution():
    values = {}
    for line in Path('/etc/os-release').read_text().splitlines():
        if '=' in line:
            key, value = line.split('=', 1)
            values[key] = shlex.split(value)[0] if value else ''
    return values


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--profile', choices=['arch', 'kali', 'server'])
    parser.add_argument('--install', action='store_true', help='explicitly install missing distribution packages')
    parser.add_argument('--optional', action='store_true', help='also check optional applications and tools')
    args = parser.parse_args()
    distro = distribution()
    profile = args.profile
    if not profile:
        chezmoi = shutil.which('chezmoi') or str(Path.home() / '.local/bin/chezmoi')
        if Path(chezmoi).is_file():
            result = subprocess.run([chezmoi, 'execute-template', '{{ .profile }}'], text=True, capture_output=True)
            if result.returncode == 0:
                profile = result.stdout.strip()
        profile = profile or ('arch' if distro['ID'] == 'arch' else 'kali' if distro['ID'] == 'kali' else 'server')
    if profile not in ['arch', 'kali', 'server']:
        parser.error('invalid configured profile')
    family = 'arch' if 'arch' in [distro['ID'], *distro.get('ID_LIKE', '').split()] else 'apt' if distro['ID'] in ['kali', 'debian', 'ubuntu'] or 'debian' in distro.get('ID_LIKE', '').split() else None
    if profile == 'arch' and family != 'arch':
        parser.error('the hardware profile requires Arch; use server or kali on this system')
    if args.install and profile == 'kali' and family != 'apt':
        parser.error('Kali package installation requires an APT guest; use checks only on the Arch reference host')
    groups = ['cli'] + (['desktop'] if profile != 'server' else []) + (['hardware'] if profile == 'arch' else [])
    entries = json.loads((REPO / 'dependencies.json').read_text())
    missing = []
    packages = set()
    for entry in entries:
        if entry['group'] not in groups or entry.get('optional', False) and not args.optional:
            continue
        present = any(shutil.which(command) for command in entry.get('commands', []))
        if entry.get('files'):
            present = any(Path(path).exists() for path in entry['files'])
        if entry.get('module'):
            present = importlib.util.find_spec(entry['module']) is not None
        if entry.get('font'):
            present = False
            if shutil.which('fc-match'):
                found = subprocess.check_output(['fc-match', '-f', '%{family}', entry['font']], text=True)
                present = entry['font'] in found
        if entry['name'] == 'chezmoi':
            present = present or (Path.home() / '.local/bin/chezmoi').is_file()
        if present:
            print('OK      ' + entry['name'])
        else:
            missing.append(entry)
            package = entry.get(family) if family else None
            if package:
                packages.update(package.split())
            print(('OPTIONAL' if entry.get('optional') else 'MISSING ') + ' ' + entry['name'] + (' -> ' + package if package else ' -> ' + entry.get('instructions', 'see docs/install.md')))
    if profile == 'arch' and shutil.which('pacman'):
        result = subprocess.run(['pacman', '-Q', 'flameshot'], text=True, capture_output=True)
        if 'native_sway' not in result.stdout:
            print('MISSING  patched Flameshot: install flameshot-native-sway; stock Flameshot cannot preserve the Arch capture workflow')
            missing.append({'name': 'patched Flameshot'})
    if shutil.which('tmux'):
        version = subprocess.check_output(['tmux', '-V'], text=True)
        match = re.search(r'(\d+)\.(\d+)', version)
        if not match or tuple(map(int, match.groups())) < (3, 3):
            print('MISSING  tmux >= 3.3 is required by the preserved configuration')
            missing.append({'name': 'tmux version'})
    print(f'Profile: {profile}; distribution: {distro["ID"]}; package family: {family or "manual"}')
    if args.install and packages:
        privilege = [] if os.geteuid() == 0 else ['sudo']
        if family == 'arch':
            # A full upgrade avoids creating an unsupported partial Arch upgrade.
            subprocess.run([*privilege, 'pacman', '-Syu', '--needed', *sorted(packages)], check=True)
        elif family == 'apt':
            subprocess.run([*privilege, 'apt-get', 'update'], check=True)
            subprocess.run([*privilege, 'apt-get', 'install', *sorted(packages)], check=True)
        else:
            parser.error('automatic package installation is only implemented for pacman and APT')
        command = [sys.executable, str(Path(__file__).resolve()), '--profile', profile]
        if args.optional:
            command.append('--optional')
        return subprocess.call(command)
    return 1 if any(not entry.get('optional') for entry in missing) else 0


if __name__ == '__main__':
    sys.exit(main())
