# PumuArch

One chezmoi source for the existing Arch Sway workstation, Kali Sway lab VMs, and Linux servers. The repository remains [PumukyDev/PumuArch](https://github.com/PumukyDev/PumuArch), on `main`, with its original Git history.

| Profile | Receives | Excludes |
| --- | --- | --- |
| `arch` | Shared CLI and Sway desktop, laptop display/audio services, native Flameshot helpers | Credentials and generated application state |
| `kali` | Shared CLI, Sway, Kitty, DMS, standard Flameshot | Physical display profiles, battery, brightness, laptop services and personal identity |
| `server` | Bash, Starship configuration, Git, the original tmux configuration, CLI helpers | Every desktop configuration and graphical service |

The desktop uses **DankMaterialShell**, which supplies the bar, launcher, notifications and clipboard history. Waybar is installed on the reference workstation but is inactive. tmux has no plugins or TPM; its original shared configuration is preserved.

## Start here

- [Installation and dependency setup](docs/install.md)
- [Architecture, daily editing, updates and security](docs/workflow.md)
- [Sway, hardware, Flameshot and SPICE validation](docs/desktop.md)
- [tmux keys, clipboard and SSH](docs/tmux.md)
- [Migration inventory, verification and recovery](docs/migration.md)

```bash
chezmoi init https://github.com/PumukyDev/PumuArch.git --promptChoice 'Profile=kali'
python3 "$(chezmoi execute-template '{{ .chezmoi.workingTree }}')/scripts/bootstrap.py" --profile kali
chezmoi diff
chezmoi apply
```

Read the installation guide first: the dependency check does not install anything, and DMS needs explicit initial setup on Kali. Choose `Profile=server` for a server. Server and Kali profiles have been rendered and tested locally; their future machines and SPICE sessions have not been deployed or tested.

## Repository layout

```text
PumuArch/
├── .chezmoiroot                 # selects home/ as the chezmoi source root
├── home/
│   ├── .chezmoi.toml.tmpl       # native initialization and profile selection
│   ├── .chezmoidata.toml        # public defaults, without identity
│   ├── .chezmoiignore           # explicit profile boundaries
│   ├── dot_bashrc, dot_bash_profile, dot_gitconfig.tmpl
│   ├── dot_tmux.conf.tmpl
│   ├── dot_config/
│   │   ├── tmux/tmux.conf       # one original shared source
│   │   ├── sway/config.d/       # common modules and small profile modules
│   │   ├── DankMaterialShell/   # common UI with profile differences
│   │   ├── kitty/, flameshot/, environment.d/
│   │   └── shikane/, systemd/, wireplumber/, waypaper/
│   └── private_dot_local/      # scripts and desktop launchers
├── dependencies.json           # executable-to-package mapping
├── scripts/                    # explicit bootstrap and validation
├── examples/systemd/           # optional fetch-only timer, disabled
└── docs/
```

Normal `chezmoi apply` and updates never install packages, run privileged commands, start services, enable timers, restart Sway, or copy secrets. No automatic update is enabled.

## Review and distribute a change

```bash
chezmoi edit ~/.config/tmux/tmux.conf
chezmoi diff
chezmoi apply ~/.config/tmux/tmux.conf
chezmoi cd
python3 scripts/validate.py
git diff
git add -A
python3 scripts/security.py --staged
git commit -m "Update shared tmux configuration"
git push origin main
```

On another machine, `dotfiles update` downloads only a fast forward when both source and managed targets are clean, displays the diff, and leaves application to `chezmoi apply`. See the workflow guide before importing changes from a rendered template.

Recovery reference: [`pre-chezmoi-20261010`](https://github.com/PumukyDev/PumuArch/tree/pre-chezmoi-20261010), pointing to `0712776d6da0a9a4fde5586ee71d63b5ab7afabb`. The original local checkout and a verified private backup also remain on the reference workstation.
