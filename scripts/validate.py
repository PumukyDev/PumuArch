#!/usr/bin/env python3
"""Render all profiles in isolated homes and validate their boundaries and syntax."""

import ast
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile

REPO = Path(__file__).resolve().parent.parent
TMUX_ORIGINAL_SHA256 = '792e118b737b9c4a6b111e363b37dee4fbda2203c663f74a7cdbac0697ad0c05'


def run(command, env=None):
    result = subprocess.run(command, env=env, text=True, capture_output=True)
    if result.returncode:
        raise RuntimeError(f'{command[0]} failed ({result.returncode}): {result.stderr or result.stdout}')
    return result.stdout


def main():
    cm = shutil.which('chezmoi') or str(Path.home() / '.local/bin/chezmoi')
    if not Path(cm).is_file():
        raise RuntimeError('Install chezmoi before validating profiles')
    shared = (REPO / 'home/dot_config/tmux/tmux.conf').read_bytes()
    # Record preservation as a migration assertion, rather than freezing future edits.
    original = hashlib.sha256(shared).hexdigest() == TMUX_ORIGINAL_SHA256
    print('Original tmux source bytes preserved:', original)
    with tempfile.TemporaryDirectory(prefix='pumuarch-validation-') as temporary:
        base = Path(temporary)
        rendered = {}
        for profile in ['arch', 'kali', 'server']:
            print('Validating', profile, flush=True)
            dest = base / profile
            dest.mkdir()
            config = base / (profile + '.toml')
            config.write_text(f'[data]\nprofile = "{profile}"\n')
            env = dict(os.environ, HOME=str(dest), XDG_CONFIG_HOME=str(dest / '.config'), XDG_DATA_HOME=str(dest / '.local/share'), XDG_STATE_HOME=str(dest / '.local/state'))
            command = [cm, '--source', str(REPO), '--destination', str(dest), '--config', str(config), '--persistent-state', str(base / (profile + '.state'))]
            run(command + ['init', '--no-tty', '--config-path', str(config), '--promptChoice', 'Profile=' + profile], env)
            run(command + ['apply'], env)
            assert not run(command + ['diff', '--no-pager'], env), 'non-idempotent profile: ' + profile
            rendered[profile] = dest
            files = {str(p.relative_to(dest)) for p in dest.rglob('*') if p.is_file() or p.is_symlink()}
            assert (dest / '.config/tmux/tmux.conf').read_bytes() == shared
            assert {'.tmux.conf', '.bashrc', '.bash_profile', '.gitconfig', '.config/starship.toml', '.local/bin/tmux-copy-pane', '.local/bin/dotfiles'} <= files
            git = (dest / '.gitconfig').read_text()
            assert '[user]' not in git and 'gpgsign = true' not in git, 'personal identity in a clone'
            if profile == 'server':
                allowed = {'.bashrc', '.bash_profile', '.bash_logout', '.gitconfig', '.tmux.conf', '.config/tmux/tmux.conf', '.config/starship.toml', '.local/bin/tmux-copy-pane', '.local/bin/dotfiles'}
                assert files == allowed, 'unexpected server files: ' + repr(files - allowed)
            else:
                assert '.config/sway/config' in files
                json.loads((dest / '.config/DankMaterialShell/settings.json').read_text())
                if shutil.which('sway'):
                    run(['sway', '-C', '-c', str(dest / '.config/sway/config')], env)
                else:
                    print('SKIP Sway executable validation: sway is unavailable')
            if profile == 'kali':
                assert not any('shikane' in f or 'wireplumber' in f or 'swayidle' in f or 'mpvpaper' in f or 'display-refresh' in f or 'audio-jack' in f for f in files)
                settings = json.loads((dest / '.config/DankMaterialShell/settings.json').read_text())
                assert 'batteryChargeLimit' not in settings
                assert 'battery' not in settings['barConfigs'][0]['rightWidgets']
                assert not settings['osdPowerProfileEnabled']
                assert not settings['lockScreenVideoPath'] and not settings['lockScreenWallpaperPath']
                for path in dest.rglob('*'):
                    if path.is_file():
                        text = path.read_text(errors='replace')
                        for value in ['/home/', 'eDP-1', 'DP-1', '2880x1800', '2560x1080', 'XF86MonBrightness', 'line_power_ACAD', 'sof_sdw']:
                            assert value not in text, f'{value} leaked into Kali: {path.name}'
            for path in dest.rglob('*'):
                if not path.is_file() or path.is_symlink():
                    continue
                text = path.read_text(errors='replace')
                if text.startswith('#!/usr/bin/env python3'):
                    ast.parse(text, filename=str(path))
                elif text.startswith('#!/usr/bin/env bash'):
                    run(['bash', '-n', str(path)])
                elif text.startswith('#!/bin/sh'):
                    run(['sh', '-n', str(path)])
            run(['bash', '-n', str(dest / '.bashrc'), str(dest / '.bash_profile')])
            run(['bash', '--noprofile', '--rcfile', str(dest / '.bashrc'), '-ic', 'test "$(alias ls)" = "alias ls=\x27ls --color=auto\x27"'], env)
            if shutil.which('tmux'):
                # A private socket and explicit files cannot alter the live server.
                socket = base / (profile + '.socket')
                tmux = ['tmux', '-S', str(socket)]
                try:
                    run(tmux + ['-f', str(dest / '.tmux.conf'), '-f', str(dest / '.config/tmux/tmux.conf'), 'new-session', '-d', '-s', 'validation', 'sleep 120'], env)
                    for option, expected in [('prefix', 'C-b'), ('mouse', 'on'), ('base-index', '1'), ('history-limit', '100000'), ('status-style', 'bg=#141218,fg=#cac4cf')]:
                        assert run(tmux + ['show-options', '-gqv', option], env).strip() == expected, option
                    keys = run(tmux + ['list-keys', '-T', 'prefix'], env)
                    assert 'wl-copy' in keys if profile == 'arch' else 'tmux-copy-pane' in keys
                    assert 'split-window -h' in keys and 'split-window -v' in keys
                    # source-file reports parse failures directly, unlike startup warnings.
                    run(tmux + ['source-file', str(dest / '.tmux.conf')], env)
                    run(tmux + ['source-file', str(dest / '.config/tmux/tmux.conf')], env)
                finally:
                    subprocess.run(tmux + ['kill-server'], env=env, capture_output=True)
            else:
                print('SKIP tmux runtime validation: tmux is unavailable')
            print(f'PASS {profile}: {len(files)} files; idempotence, boundaries, templates and available syntax/runtime checks')
        for rel in ['.config/sway/config.d/00-base.conf', '.config/sway/config.d/05-session.conf', '.config/sway/config.d/10-desktop.conf']:
            assert (rendered['arch'] / rel).read_bytes() == (rendered['kali'] / rel).read_bytes()
        # A spelling error must fail safely rather than unexpectedly install a desktop.
        config = base / 'invalid.toml'
        config.write_text('[data]\nprofile = "invalid"\n')
        result = subprocess.run([cm, '--source', str(REPO), '--config', str(config), 'managed'], capture_output=True)
        assert result.returncode != 0, 'invalid profile was accepted'
    print('PASS shared sources and invalid profile rejection')


if __name__ == '__main__':
    main()
