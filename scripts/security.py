#!/usr/bin/env python3
"""Check the proposed repository tree without printing sensitive matching content."""

import argparse
from pathlib import Path
import re
import subprocess
import sys

REPO = Path(__file__).resolve().parent.parent
PATTERNS = {
    'private key': r'-----BEGIN (?:[A-Z0-9 ]+ )?PRIVATE KEY-----',
    'GitHub token': r'\b(?:gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{30,})\b',
    'AWS access key': r'\b(?:AKIA|ASIA)[A-Z0-9]{16}\b',
    'credential URL': r'https?://[^/\s:@]+:[^/\s@]+@',
    'secret assignment': r'(?im)^\s*(?:password|passwd|api_key|access_token|auth_token|privatekey|presharedkey)\s*[:=]\s*["\x27]?[A-Za-z0-9+/=_-]{12,}',
    'machine home': r'/home/(?!\{\{)[a-z_][a-z0-9_-]*/',
    'private IPv4 address': r'\b(?:10\.(?:\d{1,3}\.){2}\d{1,3}|192\.168\.\d{1,3}\.\d{1,3}|172\.(?:1[6-9]|2\d|3[01])\.\d{1,3}\.\d{1,3})\b',
}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--staged', action='store_true', help='inspect the exact index tree to be committed')
    args = parser.parse_args()
    if args.staged:
        paths = subprocess.check_output(['git', 'ls-files', '-z'], cwd=REPO).decode().split('\0')
    else:
        paths = [str(p.relative_to(REPO)) for p in REPO.rglob('*') if p.is_file() and '.git' not in p.relative_to(REPO).parts]
    findings = []
    for rel in filter(None, paths):
        if Path(rel).name == 'security.py':
            continue  # This file contains the detection signatures themselves.
        if args.staged:
            data = subprocess.check_output(['git', 'show', ':' + rel], cwd=REPO)
        else:
            data = (REPO / rel).read_bytes()
        try:
            text = data.decode('utf-8')
        except UnicodeDecodeError:
            findings.append((rel, 'unexpected binary file'))
            continue
        for name, pattern in PATTERNS.items():
            if re.search(pattern, text):
                findings.append((rel, name))
        if any(part in {'.ssh', '.env', '__pycache__', 'obsidian', 'Bitwarden'} for part in Path(rel).parts):
            findings.append((rel, 'forbidden state or secret directory'))
    for rel, reason in findings:
        print(f'REVIEW {rel}: {reason}')
    if not findings:
        print('PASS: no detected secret signatures, private addresses, machine homes or binary state in the proposed tree')
    return bool(findings)


if __name__ == '__main__':
    sys.exit(main())
