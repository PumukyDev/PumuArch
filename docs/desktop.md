# Sway and the shared desktop

## Effective configuration

The reference Arch session uses Sway 1.12. It originally included `/etc/sway/config`, whose only active include was `/etc/sway/config.d/50-systemd-user.conf`, followed by the user's DMS overrides. Those active defaults are captured in one common module so a different distribution's defaults cannot silently change keys or start an extra bar.

| Module | Purpose |
| --- | --- |
| `00-base.conf` | Original Sway variables, movement, workspace/layout/resize keys, media keys, Print/grim and the stock bar definition |
| `05-session.conf` | Original systemd/D-Bus environment export |
| `10-desktop.conf` | Kitty, Spanish keyboard, borders, DMS bar replacement, applications, notifications, clipboard and Flameshot window rules |
| `15-remote-client.conf` | New emergency shortcut to deactivate a client's shortcut inhibitor |
| `20-arch.conf` | Touchpad taps, local video preview/autostart, native capture bindings and physical brightness |
| `20-kali.conf` | Virtual output scale 1 and standard Flameshot capture |
| `local.d/*.conf` | Optional private machine overrides, excluded from source control |

The entry point includes exactly one `20-PROFILE.conf`. Server receives no Sway files. Common modules are byte-identical between Arch and Kali. The keyboard remains `es`, `pc105`, with the original `terminate:ctrl_alt_bksp` option.

## Preserved shortcuts

`Super` is Mod4. The migration compared all 86 existing effective bindings with the original include chain. The only addition is `Super+Ctrl+Escape`, available even while a client inhibits shortcuts, to deactivate the current inhibitor.

| Shortcut | Behavior |
| --- | --- |
| `Super+Enter` | Kitty, opening/attaching the persistent `main` tmux session |
| `Super+1…0`, `Super+Shift+1…0` | Switch workspace / move window to workspace 1…10 |
| `Super+arrows`, `Super+h/j/k` | Original focus navigation; `Super+l` is the existing DMS lock override |
| `Super+Shift+arrows/h/j/k/l` | Move windows |
| `Super+r` | Original resize mode |
| `Super+b`, `Super+s/w/e` | Horizontal split, stacking, tabbed, split layout |
| `Super+Shift+Space`, `Super+a` | Floating toggle, parent focus |
| `Super+minus`, `Super+Shift+minus` | Show / move to scratchpad |
| `Super+Space`, `Alt+Space` | DMS spotlight / spotlight bar |
| `Super+v/n/m/comma/p/l` | Clipboard / notifications / processes / settings / power menu / lock |
| `Super+d/f/o/c` | Discord / Firefox / Obsidian / VS Code |
| `Super+Shift+f` | Fullscreen |
| `Super+Shift+a` | Flameshot GUI |
| `Super+Shift+s` | Native output capture on Arch; standard Flameshot GUI on Kali |
| `Super+Shift+d` | Arch internal display capture; absent on Kali |
| `Print` | Original grim screenshot |
| `Super+Shift+q/c/e` | Kill window / reload / original exit confirmation |

Thin pixel borders, smart borders, floating modifier, window layout rules, bar suppression, lock integration and audio/media controls are preserved. The application shortcuts require their listed executable; account data is not included.

## Arch displays and power

At migration time only the internal display was connected: **eDP-1, 2880x1800, scale 2, 120 Hz**, logical size 1440x900. shikane contains laptop-only, two known LG display arrangements and a generic external profile. The desk profile requests 2560x1080 at 100 Hz, scale 1, positioned to the right; the other known display requests 1920x1080 at approximately 144 Hz, above the laptop. An external connector was not present, so the historical `DP-1` name and actual two-display operation were not re-tested.

shikane requests the internal 60 Hz baseline. The existing refresh monitor then selects the highest **advertised** refresh at each active output's current resolution, without changing resolution, scale or layout, and verifies/rolls back failed mode changes. It monitors output events and the existing UPower AC object. Despite its older internal-display filename, the current code applies to every active output. This exact policy is retained, including its current behavior on battery; no new performance policy is invented.

Only Arch receives shikane, display helpers, the AC refresh monitor, physical audio-jack switching, WirePlumber display-audio policy, battery UI, brightness keys, Waypaper/mpvpaper integration and the idle screen policy. The existing system power-profiles-daemon remains a system dependency; the migration does not alter its global configuration. No active lid binding or separate AC/battery power profile script was found. Existing swayidle turns outputs off after 600 seconds, restores them on resume, and locks through DMS after 660 seconds. No new lid/suspend policy is added.

The active user services are `display-profiles`, `internal-display-refresh-rate`, `mpvpaper-visibility`, `swayidle`, `audio-jack-autoswitch` and the package-provided DMS unit. Unit paths now use `%h`; helper paths use `$HOME`. Enablement links resolve to the same units. Applying dotfiles does not start or restart them; after changing unit definitions, explicitly run `systemctl --user daemon-reload` when appropriate. The migration reloaded definitions without restarting the services.

Physical model/card names belong to this explicit Arch profile. Monitor serials and media paths stay in private local chezmoi data. Wallpapers, mpv IPC sockets, locks, cached preview images and generated shikane lock files are not source assets.

## Flameshot

Arch retains Flameshot `14.0.0.native_sway1-1`, its current INI settings and the exact `flameshot-active-screen` script. The script queries active Sway outputs and matches them to PyQt6 screen names. It prefers an external display, falls back to the internal display, and accepts `--laptop` for explicit internal capture. It then invokes `flameshot screen --number N --edit`. The monitor-selector rule floats `app_id=flameshot`, `title=flameshot`; pinned images with `title=flameshot-pin` float with no border. No source code, package or patch in [flameshot-native-sway](https://github.com/PumukyDev/flameshot-native-sway) was changed.

Kali uses its standard Flameshot package and the shared GUI/pin rules. It does not receive the physical-output helper or its laptop shortcut. Mixed-DPI native capture on Kali would require separately evaluating a compatible patch; it is not claimed here.

## SPICE from the Arch Sway host

Keyboard grabbing and shortcut inhibition must succeed **on the host**. The guest's Sway configuration cannot prevent host Sway from handling `Super+1`. A Wayland client must request the keyboard shortcuts inhibition protocol; host support alone does not activate it. Sway supports seat/client inhibitor controls, and the shared desktop provides an emergency deactivation shortcut. [Sway input commands](https://github.com/swaywm/sway/blob/master/sway/sway-input.5.scd), [Sway client commands](https://github.com/swaywm/sway/blob/master/sway/sway.5.scd).

When a VM is available, use a native Wayland viewer and explicit release/fullscreen keys:

```bash
GDK_BACKEND=wayland remote-viewer \
  --hotkeys=toggle-fullscreen=shift+f11,release-cursor=shift+f12 \
  connection.vv
```

The `.vv` connection descriptor may contain a ticket and belongs outside Git. `Shift+F12` is handled by the client while its display has focus; `Shift+F11` toggles fullscreen. Unspecified viewer hotkeys are disabled with this option, which avoids consuming unrelated Ctrl/Alt/Super combinations. See the [official remote-viewer manual](https://gitlab.com/virt-viewer/virt-viewer/-/raw/master/man/remote-viewer.pod). Use a normal disposable connection, not kiosk mode.

Enable keyboard grabbing in the viewer and give its guest display focus. With `WAYLAND_DEBUG=1` on the viewer, inspect whether a `zwp_keyboard_shortcuts_inhibit_manager_v1` inhibitor is created; keep any resulting logs private. Do not add `--inhibited` to ordinary host workspace bindings. The emergency `Super+Ctrl+Escape` is explicitly available while inhibited; click/focus another host window after release if the viewer immediately reacquires its grab. The new chord takes effect when Sway next reloads or starts; migration deliberately left the running compositor untouched.

A viewer build, GTK backend or XWayland path may fail to request inhibition. Test the actual versions before claiming capture. If native capture fails, a consciously enabled host Sway mode with no conflicting workspace bindings can be evaluated as a temporary workaround; do not globally disable host shortcuts or assume XWayland implements the same behavior. This repository does not enable such a mode automatically.

## Clipboard, mouse and resizing limitations

SPICE has an agent protocol for clipboard and display changes, but the documented Debian `spice-vdagent` is an X11 session agent: its clipboard and automatic monitor adjustments target X11. Installing it does not establish native Sway clipboard exchange or compositor output resizing. No unverified third-party bridge is installed or started. Check the actual Kali agent version and current upstream capabilities when the VM exists. [Debian agent manual](https://manpages.debian.org/trixie/spice-vdagent/spice-vdagent.1.en.html), [SPICE agent protocol](https://spice.pages.freedesktop.org/spice-space/agent-protocol.html).

Kali's output configuration assumes no connector name and fixes only scale 1. It accepts the virtual display's initial mode; it does not promise dynamic resize. `swaymsg -t get_outputs` lists the real virtual connector and advertised modes. Choose an available mode manually if guest resizing is unsupported. Smooth absolute-pointer behavior also depends on the VM's virtual device and agent. No Proxmox device was changed during migration.

## Validation when a Kali VM exists

1. Run bootstrap's Kali check in the actual guest. Confirm Sway, DMS, Kitty, fonts, clipboard and portal packages; validate `sway -C -c ~/.config/sway/config`.
2. Inspect `swaymsg -t get_outputs` and `get_inputs`: one virtual output, scale 1, Spanish layout, no reference physical display names or laptop services. Check `systemctl --user status dms sway-session.target`.
3. Open the native Wayland viewer, focus the guest, enable its grab and press `Super+1`, `Super+2`, `Super+Enter`, and representative Ctrl/Alt combinations. Guest workspaces should change while host workspaces remain fixed.
4. Test `Shift+F12`, click a host window, and confirm host keys work again. Test fullscreen with `Shift+F11` and the host emergency chord. Observe actual inhibitor negotiation if capture fails.
5. Copy harmless text in both directions between native Wayland applications. Test images separately. Also test XWayland applications to identify whether only X11 selection sharing works. Record failures instead of assuming the agent bridges Wayland.
6. Move the pointer across the guest, drag windows, scroll, change viewer size and fullscreen. Inspect guest output modes before/after; record whether resolution follows, remains fixed or needs a manual supported mode.
7. Open tmux in Kitty, test navigation, copy mode and `Prefix+Y`. Run SSH/nested-client checks separately; SPICE clipboard support and SSH OSC 52 are different transports.

For Arch manual acceptance, test the original Flameshot monitor selector, external/internal shortcuts and pinned images with both displays attached; test mixed scale 2/1, DMS launcher/lock/clipboard, unplug/replug display transitions, battery/AC events and audio-jack switching. Syntax and static preservation passed; these interactive hardware actions were not simulated during migration.
