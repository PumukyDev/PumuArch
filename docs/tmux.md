# The original tmux configuration

`home/dot_config/tmux/tmux.conf` was copied byte for byte from the active Arch configuration. Its initial SHA256 is `792e118b737b9c4a6b111e363b37dee4fbda2203c663f74a7cdbac0697ad0c05`. This records the migration baseline; future intentional edits are allowed. All profiles receive this **same file**.

The Arch rendering of `~/.tmux.conf` also matches its original bytes. It contains `Prefix+Y`, which captures the full pane history with `tmux capture-pane -p -S - | /usr/sbin/wl-copy`. On the supported tmux versions, the normal configuration search loads `~/.tmux.conf` and the XDG tmux configuration; the migration tested both files together. Use normal `tmux` startup. If using `tmux -f`, explicitly load both files, since `-f` replaces the normal configuration file list.

## Preserved behavior

| Key or option | Behavior |
| --- | --- |
| Prefix | `Ctrl+b`, unchanged |
| `Prefix+c` | New window in the current pane directory |
| `Prefix+v`, `Prefix+s` | Horizontal/vertical split in the current pane directory |
| `Prefix+arrows` | Repeatable pane focus |
| `Prefix+H/J/K/L` | Resize panes left/down/up/right |
| `Prefix+r` | Reload the shared XDG configuration and display the original notification |
| `Prefix+Y` | Copy complete pane history using the profile's clipboard transport |
| Mouse | Enabled; default selection/copy mode behavior retained |
| Indices | Windows and panes start at 1; windows renumber |
| History | 100000 lines |
| Terminal | `tmux-256color`; Kitty RGB, extended keys, hyperlinks and clipboard features |
| Status | Original dark DMS colors, session left, hostname/date/time right |
| Session lifetime | Persistent; detach does not destroy the session |

Focus events, escape time 10, passthrough, activity flags, automatic names and the original default copy key tables remain intact. No TPM, plugin directory, plugin install step or external status script was present. Bash loads Kitty integration when Kitty's installation variable exists; Kitty starts `tmux new-session -A -s main`. New Bash shells use the same aliases and Starship appearance.

## Clipboard transport

| Environment | `Prefix+Y` | Copy mode |
| --- | --- | --- |
| Arch local Sway | Original direct `wl-copy` pipeline | tmux's original `set-clipboard on`, with Kitty OSC 52 support |
| Kali local Sway | `tmux-copy-pane` chooses `wl-copy` with a local Wayland session | Same native tmux clipboard behavior |
| Kali/Server over SSH | Helper uses `tmux load-buffer -w -` to request OSC 52 on the attached client | Native tmux OSC 52 when the client advertises `Ms` |
| Headless Server | tmux buffer and OSC 52 request; no Wayland package required | No guarantee of a GUI clipboard without terminal support |
| SSH into Arch | Original `Prefix+Y` still targets Arch's local Wayland clipboard | Use ordinary tmux copy mode for OSC 52 toward the SSH client |

The helper checks `WAYLAND_DISPLAY`, `SSH_CONNECTION`, and availability of `wl-copy`. SSH takes the OSC 52 path even if a Wayland variable is inherited. Kali/Server advertise the clipboard feature for outer `tmux*` terminals, and refresh the relevant environment on reattach. Arch's original options and `Prefix+Y` are unchanged.

tmux already uses `set-clipboard on` and `allow-passthrough on`. For nested tmux, the inner instance needs `Ms` for `tmux-256color`, the outer one needs `set-clipboard on` and `Ms` for its terminal, and the physical terminal must accept OSC 52. SSH itself transports bytes; it does not provide or negotiate a system clipboard. A browser console, serial terminal, terminal multiplexer or intermediate terminal can ignore, filter or truncate clipboard sequences. [Official tmux clipboard documentation](https://github.com/tmux/tmux/wiki/Clipboard).

The installed Kitty 0.49.2 configuration loader reports its default clipboard permissions allow clipboard/primary writes and ask before reads. No older `no-append` workaround was added blindly: the current Kitty documentation describes the current options. Large copies are subject to terminal limits. `set-clipboard on` retains the existing ability for programs inside tmux to request clipboard writes. [Kitty clipboard controls](https://sw.kovidgoyal.net/kitty/conf/#opt-kitty.clipboard_control).

## Check a real SSH client

```bash
# Inside the tmux instance to diagnose:
tmux show-options -s set-clipboard
tmux info | rg 'Ms:'
infocmp -x tmux-256color
# Run outside tmux on the SSH client, then inside the remote shell as needed:
printf '%s\n' "$TERM"
```

`Ms` should show an escape sequence rather than `[missing]`. Install `ncurses-term` on Debian when the tmux terminal entry is absent. For Kitty SSH, `kitten ssh USER@HOST` can arrange the client terminfo; otherwise transfer the public terminfo definition using `infocmp -x xterm-kitty | ssh USER@HOST 'tic -x -'`. No private key is transferred by that command.

Use a disposable test string in a real remote pane, enter copy mode with `Prefix+[`, select/copy using the existing emacs copy keys or mouse, then paste into a local application. Test `Prefix+Y` on Kali/Server as well. For nested sessions use `Prefix+Prefix` to send the prefix inward. Repeat through every hop and with the actual client terminal. If `Ms` is missing, add a clipboard feature only for a terminal that really supports OSC 52, after checking its documentation; do not claim support with an unrestricted wildcard.

## Verification scope

All three profiles were loaded in separate tmux sockets on Arch. The Arch files, effective global/server options and complete key tables were compared with the active tmux server, accounting for the temporary HOME path in `Prefix+r`. Native Wayland clipboard and emitted OSC 52 behavior were checked in isolated sessions as recorded in the migration document. No remote server or nested SSH connection was opened. Real remote terminal acceptance and SPICE clipboard remain separate manual checks.
