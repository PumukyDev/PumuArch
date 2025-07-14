from libqtile.config import Key
from libqtile.lazy import lazy
#from .widgets import show_graphs

mod = "mod4"

screenshot_command = "sh -c 'scrot --select --line mode=edge /tmp/screenshot.png && xclip -selection clipboard -t image/png -i /tmp/screenshot.png && echo /tmp/screenshot.png >> /home/adrian/.cache/greenclip.history'"
#borrar_foto = "mv /tmp/screenshot.png /tmp/screeshot_antigua.png"
borrar_foto = "rm -f /tmp/screenshot.png"


#ATAJOS DE TECLADO
keys = [
    #Moverse entre ventanas
    Key([mod], "Left", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "Right", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "Down", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "Up", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "Tab", lazy.layout.next(), desc="Move window focus to other window"),

    #Mover ventanas
    Key([mod, "shift"], "Left", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "Right", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], "Down", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "Up", lazy.layout.shuffle_up(), desc="Move window up"),

    #Cambiar tamaño ventanas
    Key([mod, "control"], "Left", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key([mod, "control"], "Right", lazy.layout.grow_right(), desc="Grow window to the right"),
    Key([mod, "control"], "Down", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "Up", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),

    #Reiniar/cerrar sesión qtile
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),

    #Varios
    Key([mod], "l", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "q", lazy.window.kill(), desc="Kill focused window"),
    Key([mod, "shift"], "f", lazy.window.toggle_fullscreen(), desc="Toggle fullscreen on the focused window"),
    Key([mod], "t", lazy.window.toggle_floating(), desc="Toggle floating on the focused window"),
    Key([mod], "r", lazy.spawncmd(), desc="Spawn a command using a prompt widget"),
    Key([mod, "shift"], "Return", lazy.layout.toggle_split(), desc="Toggle between split and unsplit sides of stack",),

    # Teclas de volumen
    Key([], "XF86AudioLowerVolume", lazy.spawn("pamixer --decrease 2")),
    Key([], "XF86AudioRaiseVolume", lazy.spawn("pamixer --increase 2")),
    Key([], "XF86AudioMute", lazy.spawn("pamixer --toggle-mute")),


    # Teclas de brillo
    Key([], "XF86MonBrightnessUp", lazy.spawn("xbacklight -inc 10")),
    Key([], "XF86MonBrightnessDown", lazy.spawn("xbacklight -dec 10")),


    #Lanzar aplicaciones
    Key([mod], "Return", lazy.spawn("kitty"), desc="Launch terminal"),
    Key([mod], "f", lazy.spawn("firefox"), desc="Launch Firefox"),
    Key([mod], "m", lazy.spawn("rofi -show drun"), desc="Launch rofi"),
    Key([mod], "c", lazy.spawn("code"), desc="Launch VSCode"),
    Key([mod], "v", lazy.spawn("virtualbox"), desc="Launch VirtualBox"),
    Key([mod], "s", lazy.spawn("steam"), desc="Launch Steam"),
    Key([mod], "t", lazy.spawn("tor-browser"), desc="Launch Tor"),
    Key([mod], "b", lazy.spawn("gnome-boxes"), desc="Launch Tor"),
    Key([mod], "a", lazy.spawn("azure"), desc="Launch Azure"),
    Key([mod], "d", lazy.spawn("discord"), desc="Launch Azure"),
    Key([mod], "p", lazy.spawn("Screeshot"), desc="Launch Azure"),
    Key([mod], "o", lazy.spawn("/home/Adrian/.config/qtile/scripts/launch_obsidian_dropbox.sh"), desc="Launch Azure"),
    Key([mod], "k", lazy.spawn("/home/Adrian/.config/qtile/scripts/launch_keepassxc_dropbox.sh"), desc="Launch Azure"),


    #Configuración Scrot
    Key([], "Print", lazy.spawn("scrot /home/Adrian/Screenshots/%d-%m-%Y-%T-screenshot.png")),
    Key([mod, "shift"], "Print", lazy.spawn("scrot --focused --border /home/Adrian/Screenshots/%d-%m-%Y-%T-screenshot.png")), 
    Key([mod], "g", lazy.spawn("rofi -modi 'clipboard:greenclip print' -show clipboard -run-command '{cmd}'"), desc="Launch rofi"),
    Key([mod, "shift"], "s", lazy.spawn("/home/adrian/.config/qtile/scripts/captura_pantalla.sh")),
 
    Key([mod, "shift"], "l", lazy.spawn("flameshot gui")),
 
    #Lanzar popup grupos de trabajo
    #Key([mod], "Tab", lazy.function(show_graphs)),
 ]

