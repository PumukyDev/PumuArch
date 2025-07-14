#IMPORTACIONES PARA LA CONFIGURACIÓN DE QTILE
import os
import subprocess
from libqtile import hook
from typing import List # noqa: F401
from libqtile import bar, layout, widget
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal
import os.path as path


from settings.keys import mod, keys


from settings.groups import groups


from settings.layouts import layouts


from settings.screens import screens


from settings.mouse import mouse





dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
floats_kept_above = True
cursor_warp = False
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True
auto_minimize = True
wl_input_rules = None
wmname = "LG3D"





@hook.subscribe.startup_once
def autostart():
    script = os.path.expanduser("~/.config/qtile/autostart.sh")
    subprocess.run([script])



