# Installation

## Prerequisites and verified user tools

Use Linux, Git, Bash, Python 3 and tmux **3.3 or newer**. chezmoi 2.73.0 or newer is required; 2.73.0 was used for the migration. Package managers are preferred; for example, on Arch use `sudo pacman -Syu --needed chezmoi git tmux python`. Check package availability on Debian/Kali rather than assuming that every release contains chezmoi or Starship.

When a distribution lacks chezmoi, clone the same repository locally and use the explicit installer:

```bash
git clone https://github.com/PumukyDev/PumuArch.git ~/.local/share/chezmoi
python3 ~/.local/share/chezmoi/scripts/install-user-tool.py chezmoi
export PATH="$HOME/.local/bin:$PATH"
```

The installer downloads a pinned asset from the official GitHub release, compares it with the release's SHA256 list, and atomically installs the binary in `~/.local/bin`. It executes no downloaded shell script and requires no root access. It supports x86_64, aarch64 and supported ARM/i386 assets. The checksums establish integrity relative to the official HTTPS release; they are not an independent signature verification. [Official chezmoi installation and verification](https://www.chezmoi.io/install/).

Optional tools, also explicit and verified:

```bash
python3 ~/.local/share/chezmoi/scripts/install-user-tool.py starship
# Desktop clients only, when the Nerd Font is missing:
python3 ~/.local/share/chezmoi/scripts/install-user-tool.py firacode
```

Pinned releases are chezmoi 2.73.0, Starship 1.26.0 and Nerd Fonts 3.5.1. Update the pins deliberately when needed. ARM binaries and fresh Debian/Kali package installation have not been exercised on this Arch workstation. See [Starship](https://starship.rs/guide/) and [Nerd Fonts releases](https://github.com/ryanoasis/nerd-fonts/releases).

## Select a profile

```bash
chezmoi init https://github.com/PumukyDev/PumuArch.git --promptChoice 'Profile=kali'
```

Use `arch`, `kali` or `server`. Initialization guesses Arch and Kali from `/etc/os-release`, and otherwise defaults to Server. An explicit selection is preferable for templates and servers. Initialization renders local `~/.config/chezmoi/chezmoi.toml` but does not apply dotfiles. An invalid profile fails before installing files.

To deliberately change an existing profile, edit `profile` in `chezmoi edit-config`, inspect `chezmoi managed` and `chezmoi diff`, and review files from the previous profile. Ignoring a previously managed graphical file does not remove an existing local file: switching an installed desktop host to Server requires conscious cleanup. New Server installations never receive those files.

## Arch

The reference workstation is already initialized with private data preserving its Git identity, display serial matching, wallpaper selection and lock screen paths. On another physical Arch host:

```bash
chezmoi init https://github.com/PumukyDev/PumuArch.git --promptChoice 'Profile=arch'
python3 "$(chezmoi execute-template '{{ .chezmoi.workingTree }}')/scripts/bootstrap.py" --profile arch --optional
# Explicitly install missing distribution packages only when desired:
python3 "$(chezmoi execute-template '{{ .chezmoi.workingTree }}')/scripts/bootstrap.py" --profile arch --install --optional
chezmoi edit-config
chezmoi diff
chezmoi apply
```

The Arch profile contains the reference laptop's hardware policies. Adapt shikane display matching and the audio card constants before deploying to different hardware. `displaySerials` holds the two optional monitor serials locally. Empty wallpaper data disables mpvpaper autostart; set `archWallpaperPath`, `archPreviewPath`, `lockScreenVideoPath` and `lockScreenWallpaperPath` locally to real files. Media and generated previews are outside Git. The Waypaper configuration is a creation-only seed; afterward its GUI owns the selection.

Keep the native patched Flameshot package from [flameshot-native-sway](https://github.com/PumukyDev/flameshot-native-sway). Bootstrap reports a missing patch and never substitutes the stock Arch package. mpvpaper is an existing local build from [GhostNaN/mpvpaper](https://github.com/GhostNaN/mpvpaper); install/build it separately on a fresh host using its upstream instructions. The Python capture helper needs PyQt6.

## Kali VM

No Proxmox or VM deployment is performed by this repository. In a future Kali VM, under the intended clone user:

```bash
chezmoi init https://github.com/PumukyDev/PumuArch.git --promptChoice 'Profile=kali'
python3 "$(chezmoi execute-template '{{ .chezmoi.workingTree }}')/scripts/bootstrap.py" --profile kali --optional
python3 "$(chezmoi execute-template '{{ .chezmoi.workingTree }}')/scripts/bootstrap.py" --profile kali --install
```

`--install` installs only missing mapped APT packages. DMS and dgop need an explicit upstream installation when absent from configured Kali repositories. Start with `apt-cache policy dms quickshell dgop`, then follow the [official DMS installation guide](https://danklinux.com/docs/dankmaterialshell/installation). It documents Debian packages and a source installation for other distributions. Confirm compatibility with the actual Kali release; bootstrap deliberately does not add Debian repositories to Kali. Source installation currently requires Go 1.26+, Quickshell, the DMS repository with its submodules, and the upstream build/install procedure. Do not run `dms setup`: the Sway configuration is supplied by this repository.

Use the explicit Nerd Fonts installer if FiraCode Nerd Font Mono is unavailable from APT. Material Symbols is a DMS dependency reported by bootstrap; follow upstream font instructions if absent. Firefox ESR is the mapped Kali browser. Standard Flameshot is used on Kali; the Arch native helper is excluded. Discord, Obsidian and VS Code are optional upstream applications. Their shared shortcuts remain familiar and require the respective executable; no accounts, vaults or application sessions are copied. Neovim, fd, fzf, ripgrep, btop and Starship are optional CLI additions from the actual reference system.

After dependencies pass:

```bash
chezmoi diff
chezmoi apply
systemctl --user daemon-reload
bash "$(chezmoi execute-template '{{ .chezmoi.workingTree }}')/scripts/configure-desktop.sh"
```

The desktop preferences command explicitly sets the reference Adwaita theme, icons, cursor, font preference and dark color scheme. It is never part of routine updates. Use the existing login manager's Sway session or launch Sway from an appropriate local TTY session with a user D-Bus bus. The shared Sway startup exports the environment and starts `sway-session.target`; its managed symlink activates the portable DMS unit. Do not enable DMS globally as a second startup mechanism. Validate the actual graphical session and SPICE capabilities using [desktop.md](desktop.md).

For SPICE, `sudo apt-get install spice-vdagent` is optional initial guest preparation. The classic agent's X11 integration does not guarantee native Sway clipboard or dynamic output resizing. It is not autostarted by these dotfiles. See the separate remote validation steps.

## Server

```bash
chezmoi init https://github.com/PumukyDev/PumuArch.git --promptChoice 'Profile=server'
python3 "$(chezmoi execute-template '{{ .chezmoi.workingTree }}')/scripts/bootstrap.py" --profile server
python3 "$(chezmoi execute-template '{{ .chezmoi.workingTree }}')/scripts/bootstrap.py" --profile server --install
# Optional development/navigation tools from the reference workstation:
python3 "$(chezmoi execute-template '{{ .chezmoi.workingTree }}')/scripts/bootstrap.py" --profile server --install --optional
chezmoi diff
chezmoi apply
```

Servers receive no font installation, compositor, desktop applications, GUI environment variables, power service or user graphical unit. Bash retains the reference aliases and uses its original fallback prompt when Starship is absent. No login shell is changed automatically; Kali may start with Zsh, so launch `bash` first and use `chsh -s /bin/bash` only if that user's preference is Bash. The same applies to existing server users.

Configure each user's Git identity locally. SSH keys, VPN profiles, tokens and homelab identities are never part of a clone or template. If editing is needed, authorize each user's own GitHub credential or push a branch from a separately authorized workstation. No publisher credentials are provisioned to templates.

## Dependency check semantics

`dependencies.json` maps real referenced programs to pacman/APT names and marks optional tools. `bootstrap.py` identifies the OS/profile, checks commands/modules/fonts and the required tmux version, and returns a failure for required omissions. It does not test guest package availability by inspecting Arch, and a successful check on Arch is not evidence of a Kali installation. Unmapped tools are reported with their installation source. Explicit package installation uses pacman with a full upgrade or APT, and leaves privileged prompts to the package manager. Normal chezmoi operations contain no bootstrap hook.

## Local profile validation

```bash
chezmoi cd
python3 scripts/validate.py
```

This creates temporary homes, tests initialization, renders all profiles twice, checks exact Server contents and Kali exclusions, validates shared sources, parses scripts and available Sway/tmux syntax, and checks key tmux behavior in private sockets. Sway execution is skipped when unavailable on a CLI-only host. Actual guest dependencies, graphics, mouse, keyboard capture and clipboard still require testing on the eventual VM.
