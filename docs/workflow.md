# Architecture and daily workflow

## Source of truth

The Git working tree is normally `~/.local/share/chezmoi`. `.chezmoiroot` selects its `home/` directory as the effective source state. `chezmoi source-path` therefore returns `.../chezmoi/home`; `chezmoi cd` opens the Git working tree, and `chezmoi execute-template '{{ .chezmoi.workingTree }}'` returns that root for scripts and documentation.

Native source names map to destinations: `dot_config` becomes `.config`, `executable_` sets executable permissions, `symlink_` stores a link destination, `.tmpl` renders a template, and `create_` initializes a file only when absent. `private_dot_local` and `private_share` preserve the reference workstation's private directory permissions. No `exact_` directory or removal script deletes unrelated local files.

Plain shared files are preferred. The original tmux file, Bash aliases, Starship appearance, Kitty settings, Sway keys and window rules have a single source. Small templates select a profile include, remove battery UI on Kali, render a few host paths, adapt tmux clipboard transport, and omit personal Git identity when unset. `.chezmoiignore` controls which destination paths a profile receives. Invalid profiles abort. [Native machine differences](https://www.chezmoi.io/user-guide/manage-machine-to-machine-differences/), [source root](https://www.chezmoi.io/reference/special-files/chezmoiroot/) and [initialization](https://www.chezmoi.io/user-guide/setup/).

## Local data and application generated files

`~/.config/chezmoi/chezmoi.toml` is private and untracked. Its `[data]` chooses `profile`, `displaySerials` and optional wallpaper/lock screen paths. `[data.gitIdentity]` stores optional `name`, `email` and the path to an SSH **public** signing key. The public defaults contain no personal identity. Edit local data with `chezmoi edit-config`; compare with `chezmoi diff` before applying. No credential is requested or embedded during initialization, and `chezmoi init` retains existing local values.

Private overrides can live in `~/.config/bash/local.bash`, `~/.config/git/local.conf`, and `~/.config/sway/local.d/*.conf`. These paths are read by the configuration but are outside the managed source state. Add files there intentionally and never `chezmoi add` them without a privacy review. tmux's shared file remains unchanged; load deliberate private tmux overrides explicitly with `tmux source-file ~/.config/tmux/local.conf` after startup if needed.

DMS palette outputs, its generated audio alias, and Waypaper's configuration are `create_` seeds. They are initialized on a fresh desktop but existing values are preserved, and `chezmoi diff` does not report later application-generated changes to these files. Deliberate UI preferences in DMS `settings.json` are managed: if changed through its UI, review the source template and edit the corresponding common setting rather than replacing the entire template. The wallpaper video, images and first-frame cache are not stored in Git.

## Edit the source first

```bash
chezmoi edit ~/.config/tmux/tmux.conf
chezmoi diff
chezmoi apply ~/.config/tmux/tmux.conf
tmux source-file ~/.config/tmux/tmux.conf
```

For Sway, use `chezmoi edit ~/.config/sway/config.d/10-desktop.conf`, review/apply, then run `sway -C -c ~/.config/sway/config`. Reload only after validation and at a convenient moment. Reloading Sway executes `exec_always`, including Arch's wallpaper restoration.

Editing the tmux source changes all profiles. Editing the common Sway modules changes Arch and Kali. Editing `20-arch.conf` or shikane affects Arch only. If a change should belong only to one host, use local data or a private override instead of making the shared source depend on that host's username.

## Import an edit made in HOME

```bash
chezmoi status
chezmoi diff
chezmoi source-path ~/.config/tmux/tmux.conf
# This destination is backed by a plain shared file:
chezmoi re-add ~/.config/tmux/tmux.conf
chezmoi git diff
```

Do not use a blanket `chezmoi re-add`. First inspect the source filename. If it ends in `.tmpl`, edit it with `chezmoi edit` and move only the intended common change into it. Importing rendered Arch paths or UI values can destroy profile logic or expose identity. For creation-only palettes, intentionally update the seed source when you want new installations to inherit a new palette; existing generated files remain owned by their application.

## Review, commit and publish

```bash
chezmoi cd
git status --short --branch
git diff
python3 scripts/validate.py
git add -A
git diff --cached --stat
git diff --cached
python3 scripts/security.py --staged
git fetch origin
# Confirm a clean, current branch; resolve divergence before pushing.
git status --short --branch
git commit -m "Describe the shared configuration change"
git push origin main
```

If new remote work exists, do not push over it. Commit your reviewed work, merge `origin/main` consciously (or rebase only unpublished local commits), resolve conflicts in **source templates**, rerun validation, and push normally. No force push or published history rewriting is required. Branches and pull requests can also be used inside the same repository.

On Kali or a server, the same editing workflow applies. Give that user's Git identity and authentication their own local configuration. A public HTTPS clone is sufficient to download; it does not grant publication rights. SSH/GitHub credentials are never shared through dotfiles.

## Update another machine

```bash
dotfiles status
dotfiles update
chezmoi apply
```

`dotfiles update` refuses to proceed when source files or managed targets have local changes. It fetches, merges only a fast forward, and prints the destination diff without applying. Review before the separate application command. For native chezmoi operations, `chezmoi update --apply=false` downloads first and `chezmoi diff` shows the pending changes; understand the configured Git pull behavior if the local branch has diverged.

When drift is intentional, import a plain file or edit the template and commit it first. When drift should be discarded, recover it in a private backup, inspect the exact affected target, and apply only that target. `chezmoi merge` and `chezmoi merge-all` can help compare source, target and previously applied state; keep profile conditions when resolving conflicts.

## Add an application, host or profile

For an application, identify its active deliberate settings, audit them, and use `chezmoi add PATH`. Inspect the resulting Git diff and source attributes. Add executable/package mappings to `dependencies.json`, profile exclusions to `.chezmoiignore`, and a boundary assertion if it introduces a new desktop path. Avoid adding caches, databases, histories or session directories.

A new host uses the existing profile and a fresh local config with no copied identity. A new profile requires adding the choice to initialization, the allowed-profile guard and relevant conditions/exclusions, bootstrap groups, validation scenarios and documentation. Keep common sources intact. Profile changes do not clean up previous installations automatically.

## Optional periodic checking

Manual updating is the default. No login update hook or enabled timer exists. `examples/systemd` provides an opt-in timer that fetches and logs pending commits, without merging, applying, installing, or restarting anything:

```bash
chezmoi cd
systemctl --user link "$PWD/examples/systemd/dotfiles-check.service" "$PWD/examples/systemd/dotfiles-check.timer"
systemctl --user daemon-reload
systemctl --user enable --now dotfiles-check.timer
journalctl --user -u dotfiles-check.service
# Disable later:
systemctl --user disable --now dotfiles-check.timer
```

The example assumes the standard working tree location. Adjust it for another location. Automatic application at login or while working would change the active configuration without a review window, so it is intentionally not implemented.

## Security review

Never add SSH private keys, Git credentials, VPN profiles, HTB/THM credentials, WireGuard secrets, `.env`, browser/account state, clipboard history, Obsidian data, shell history, cookies or databases. Keep secrets outside Git, including encrypted secrets for this first version. `.gitignore` is only a guard against accidental staging; tracked content still needs review. Profile exclusions are not a secrecy mechanism: every source file in a public repository is public.

`scripts/security.py --staged` checks the actual index for known secret formats, credential URLs, machine-specific homes, private IPv4 addresses and unexpected binary data, reporting only paths and categories. Manually inspect every staged file as well. During migration, Gitleaks 8.30.1 scanned both the replacement source tree and the existing two-commit history with redaction and found no secret signatures. Neither scanner proves absence of every possible secret. Private backup archives and local profile data are never uploaded.
