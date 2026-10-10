# Migration and recovery

## Original inventory

Inspection on 2026-10-10 used the live Arch workstation as the authority, not the old Qtile repository. Arch is rolling; Sway 1.12 ran in a Wayland session, using the user's `.config/sway/config` plus the distribution config and its systemd environment include. Bash was the login shell, Starship 1.26.0 supplied the prompt, and Kitty 0.49.2 opened the persistent tmux `main` session. tmux 3.8 used the root clipboard binding and the XDG custom configuration, without TPM or plugins.

The actual shell/bar/launcher/notification system was DMS 1.6.3 with Quickshell 0.3.2, rather than Waybar. Thunar was installed as the file manager. Firefox, Discord, Obsidian and VS Code were bound in Sway. Search/navigation tools included ripgrep, fd, fzf and Neovim, but no deliberate Neovim/Vim configuration was present. Foot was retained for the display-profile dialog. Alacritty, Fish, Rofi, Dunst, Picom and Qtile in the old checkout were not active authorities.

The active keyboard layout was Spanish. The only connected panel was eDP-1 at 2880x1800, scale 2 and 120 Hz. shikane stored the external-display arrangements; a refresh monitor selected advertised rates, and user services managed displays, wired-audio switching, idle locking and animated-wallpaper visibility. System power-profiles-daemon and NetworkManager were active. No separate active lid binding, NVIDIA assumption or obsolete Qtile power script was imported.

Adwaita was the GTK/icon/cursor preference, Adwaita Sans 11 the font preference, with dark color scheme. Kitty used FiraCode Nerd Font Mono. Qt was set to Wayland with the GTK3 platform theme. DMS generated the theme color files. Flameshot was the native Sway patched package with the current Python capture helper, INI preferences and floating/pin rules.

## Classification and scope

| Classification | Treatment |
| --- | --- |
| Active deliberate configuration | Migrated from live HOME; behavior preserved |
| Installed but unused desktop configuration | Not made authoritative; documented rather than copied blindly |
| Obsolete Qtile/Stow tree | Removed from the new repository tree, retained in history and recovery tag |
| Generated theme files and audio alias | Creation-only seeds; application retains ownership afterward |
| Wallpaper media and preview cache | Kept local; paths represented by private machine data |
| Histories, caches, session state, databases | Excluded |
| SSH/Git/account/VPN credentials and Obsidian content | Excluded; no new secret management system introduced |
| Physical card/output/AC policies | Arch only; monitor serials kept in local data |
| Existing symlinks | Inventoried; user-service links retained with equivalent portable destinations |

No existing Stow links managed the selected live dotfiles. The original local checkout had 30 tracked changes/deletions and six untracked groups; all were backed up privately and the checkout remains intact. It was not reset or cleaned. A separate local clone of **the same existing GitHub repository** became chezmoi's working tree. No new GitHub repository was created.

## Repository replacement

The previous tree had 212 tracked files arranged by application, including 62 Qtile files and 119 font/font-cache files. All 212 old tracked paths were replaced by the new idiomatic chezmoi tree. The old top-level groups were Code, Alacritty, Bash, display-manager state, Dunst, Firefox profiles, Fish, fonts, Git, GTK, Kitty, Picom, Qtile and Rofi. Old X11 display layouts, lock/power helpers, target/interface state, compiled/cache artifacts, browser profile identifiers, redundant theme assets and bundled fonts were removed from the new tree.

Relevant Bash, Git and Kitty functionality was re-derived from the live system. Current Sway/DMS, tmux, Flameshot, monitor/audio/idle scripts and portable user services replaced the old content. Package dependencies replace bundled fonts; a verified optional Nerd Font installer is available. Old Firefox/account/editor state was not copied. No repository history was rewritten, no remote branch removed, no visibility/name change made, and no force push used.

## Recovery points created before source changes

- Annotated tag `pre-chezmoi-20261010`, published in PumuArch and verified by remote lookup, points to original `main` commit `0712776d6da0a9a4fde5586ee71d63b5ab7afabb`.
- A Git archive of that tag was generated, and a complete history bundle passed `git bundle verify`.
- A private archive at `~/.local/state/pumuarch-backups/20261010-145619/original-home.tar.gz` contains the selected original HOME files, symlinks and the complete dirty local checkout. Every regular archive member was compared by SHA256 with its original source. The directory is mode 700 and the archive mode 600.
- `~/.local/state/pumuarch-backups/latest` records the local backup path. The original checkout remains at `~/desktop/PumuArch`.

Backup archives contain private machine data and must never be uploaded. The Git tag recovers published history; the private archive additionally recovers the original uncommitted local work and live configuration.

## Verified outcomes

The common tmux file's bytes and Arch's root tmux file are unchanged. A separate server with the rendered Arch files matched the running tmux server's complete key tables and global/server options, normalizing only the temporary HOME path in the reload binding. All 86 original effective Sway bindings matched; the native Flameshot window rules matched. The new host emergency inhibition shortcut is additive. DMS's rendered Arch settings were parsed and compared with the active original JSON, with no semantic change.

The initial apply installed Sway modules first, validated Sway, then applied the reviewed managed set with conflict errors enabled. Sway validated again; `chezmoi diff` was empty and `chezmoi verify` passed. Display mode, scale, position, input configuration, service states and service PIDs were compared before/after and did not change. The native Flameshot helper's SHA256 and all relevant Git identity/signing values were preserved. Sway was not reloaded, restarted or logged out. systemd unit definitions were verified and reloaded without service restarts. No automatic timer was enabled.

`scripts/validate.py` passed on isolated temporary homes: Arch rendered 55 managed files, Kali 31 and Server 9. It checked initialization, template syntax, idempotent rendering/application, shared file identity, invalid-profile rejection, exact Server inventory, Kali hardware/identity exclusions, Bash startup, script syntax, Sway configuration validation and tmux runtime options/keys on separate sockets.

Clipboard tests used a separate headless Sway compositor with its own runtime directory. The **original** Arch full-pane `wl-copy` pipeline round-tripped the expected bytes through `wl-paste` without changing the active session clipboard. A separate tmux client attached to a pseudo-terminal advertised as Kitty received the expected OSC 52 sequence; the installed remote helper also emitted the correct full-pane payload. This verifies transport generation, not a future physical terminal's acceptance.

The user installers downloaded and verified chezmoi, Starship and FiraCode releases into a disposable HOME. Their binaries ran, and a second chezmoi installation changed zero files. Arch's required dependency check passed, including the custom Flameshot package and fonts. Optional SPICE viewer/guest-agent executables were absent and were not installed. No sudo password was needed: the current chezmoi binary was installed as a verified user executable, and no global package change was made.

Both the new working tree and the pre-existing two-commit history passed Gitleaks 8.30.1 with redaction. The staged tree additionally passed the repository's content/privacy scan, a manual content review and an English-language audit. Private profile data and backups stayed outside Git. Secret detection is evidence from the tools and review, not a mathematical guarantee.

## Interactive checks still required when relevant

Future Kali/Server systems were not deployed or contacted. Proxmox, PI1 and other remote hosts were not changed. Their package compatibility, hardware/drivers, real SSH terminal acceptance, nested SSH routes and SPICE behavior require testing in those actual environments. Use the prepared installation and validation guides.

The external monitor was disconnected during migration. Reconnect it at a convenient time and verify the preserved shikane arrangement and mixed-DPI Flameshot actions. Full visual capture/pin interaction, physical battery/AC transitions, brightness keys, lock transitions and wired-jack actions were not triggered during this non-disruptive migration. The current live session kept its pre-migration settings; the modular configuration has passed syntax and semantic comparisons for the next reload/start.

## Rollback

To inspect the original published repository without disturbing the current source:

```bash
chezmoi cd
git worktree add --detach ../pumuarch-before-chezmoi pre-chezmoi-20261010
```

That old tree is not a chezmoi source. Do not initialize/apply it as if it were the new layout.

To restore selected live files from the private archive, first save any post-migration edits and inspect the archive list. For example:

```bash
backup=$(cat "$HOME/.local/state/pumuarch-backups/latest")
tar -tzf "$backup/original-home.tar.gz"
# Restore only the files you have reviewed:
tar -xzf "$backup/original-home.tar.gz" -C "$HOME" -- \
  .config/sway/config .config/tmux/tmux.conf .tmux.conf
sway -C -c ~/.config/sway/config
```

The original Sway entry point uses the unchanged system include chain. Extra modular files are harmless when that original entry point is restored. Restore specific shell/scripts/units from the same archive if needed; verify before reloading services or Sway. Avoid extracting the complete dirty checkout over new work without first reviewing what it would overwrite. Stop routine chezmoi application while investigating a rollback; no automation is enabled that could undo the restoration unexpectedly.

For later shared configuration regressions, use `git restore --source=GOOD_COMMIT -- home/PATH` or `git revert BAD_COMMIT`, review the new diff, validate and publish a normal corrective commit. Apply the reviewed correction on each relevant profile. The recovery tag and history remain available; no destructive history rewrite is necessary.
