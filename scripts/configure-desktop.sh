#!/usr/bin/env bash
# Explicit initial setup only; this is never run by chezmoi apply or update.
set -euo pipefail
profile=$(chezmoi execute-template '{{ .profile }}')
case $profile in
    arch|kali) ;;
    *) printf 'Desktop preferences require the arch or kali profile.\n' >&2; exit 1 ;;
esac
gsettings set org.gnome.desktop.interface gtk-theme 'Adwaita'
gsettings set org.gnome.desktop.interface icon-theme 'Adwaita'
gsettings set org.gnome.desktop.interface cursor-theme 'Adwaita'
gsettings set org.gnome.desktop.interface font-name 'Adwaita Sans 11'
gsettings set org.gnome.desktop.interface color-scheme 'prefer-dark'
