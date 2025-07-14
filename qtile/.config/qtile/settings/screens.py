import os
from libqtile.config import Screen
from libqtile import bar, widget
from libqtile.lazy import lazy
from libqtile import qtile
import subprocess

# Ruta del archivo de configuración
state_file = os.path.expanduser("~/.config/qtile/themes/environment/current_environment.txt")

# Función para leer el estado desde el archivo
def read_environment():
    if os.path.exists(state_file):
        with open(state_file, "r") as file:
            return file.read().strip()
    return "arch"  # Valor predeterminado

# Función para escribir el estado en el archivo
def write_environment(environment):
    with open(state_file, "w") as file:
        file.write(environment)

# Leer el entorno actual desde el archivo
current_environment = read_environment()

# Funciones para cambiar el entorno
def set_environment_to_arch(qtile):
    write_environment("arch")
    subprocess.run(["feh", "--bg-scale", os.path.expanduser("~/.config/qtile/themes/wallpapers/japanese.jpg")])
    qtile.cmd_reload_config()  # Recarga la configuración de Qtile

def set_environment_to_black_arch(qtile):
    write_environment("black_arch")
    subprocess.run(["feh", "--bg-scale", os.path.expanduser("~/.config/qtile/themes/wallpapers/red_mountains.jpg")])
    qtile.cmd_reload_config()  # Recarga la configuración de Qtile



programas = {
        'firefox': 'firefox',
        'terminal': 'alacritty',
        'editor': 'code',
        'thunar': 'thunar',
        'steam':'steam',
        'tor':'Tor Browser',
        'a':'a',
        'b':'b',
        'c':'c',
        'd':'d',
        'e':'e',
        'f':'f',
        'g':'g',
        'h':'h',
        'i':'i',
        'j':'j',
        'k':'k',
    }

sex={
    'steam':'steam',
        'tor':'Tor Browser',
        'a':'a',
        'b':'b',
        'c':'c',
        'd':'d',
        'e':'e',
        'f':'f',
        'g':'g',
        'h':'h',
        'i':'i',
        'j':'j',
        'k':'k',
}



def show_program_menu(qtile, program_list):
    menu_options = "\n".join(program_list.keys())
    rofi_command = "rofi -theme+window+width 18% -dmenu -p 'Selecciona un programa' -lines {0} -location 1 -yoffset 46".format(len(program_list))
    rofi_process = subprocess.Popen(rofi_command, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    selected_program = rofi_process.communicate(input=menu_options.encode())[0].decode().strip()
    if selected_program in program_list:
        programa_path = program_list[selected_program]
        qtile.cmd_spawn(programa_path)





# Función para mostrar la notificación sin depender de Qtile
def mostrar_bateria():
    subprocess.run(['notify-send', 'Batería', 'Probando la notificación'])

with open(os.path.expanduser('~/.config/qtile/themes/environment/current_interface.txt')) as f:
    interface = f.read().strip()

# Barra para Arch
def arch_bar():
    return bar.Bar(
        [
            widget.Image(
                filename="~/.config/qtile/themes/icons/Icono_Arch.png",
                margin_x=12,
                margin_y=4,
                mouse_callbacks = {
                'Button3': lazy.function(set_environment_to_black_arch),
                'Button2': lazy.function(show_program_menu, programas),
                },
                #mouse_callbacksDict of mouse button press callback functions. Accepts functions and lazy calls.),
                scale=True,
                #width=20,
            ),
            #widget.TextBox("I use arch BTW", font="FiraCode Bold"),
            #Idea a implementar para el icono --> Como hay una función mouse_callback, puedo hacer que al darle al icono de arch, se ent>
            widget.Prompt(),
            widget.TextBox("", width=bar.STRETCH),
            widget.Clock(
                format="%d/%m/%Y %A %H:%M",
                fontsize=13,
                font='Helvetica '
                #foreground='#bfbfbf',
            ),
            widget.TextBox("", width=bar.STRETCH),
            #widget.Battery(format="{percent:2.0%}"),
            widget.CheckUpdates(
                display_format='󰇚 {updates}  |',
                colour_have_updates='#bfbfbf',
                execute='kitty -e /usr/bin/pacman -Syu', 
                no_update_string='',
                fontsize=15,
                padding=8,
            ),
            #widget.Cmus(),
           widget.Wlan(
                interface='wlan0',
                ethernet_interface='enp3s0f3u1c2',
                fontsize=16,
                disconnected_message='',
                format=' ',
                foreground='#bfbfbf',
                padding=7,
                mouse_callbacks={
                    'Button1': lazy.spawn('sh -c \'notify-send "Batería" "$(acpi | cut -d, -f2)"\''),
                 }
            ),
            widget.Net(
                
                interface=interface,
                fontsize=20,
                format='󰈀',
                foreground='#bfbfbf',
                use_bits=False,
                update_interval=1,
                padding=6,
                mouse_callbacks={
                    'Button1': lazy.spawn('sh -c \'notify-send "IP" '+str(interface)+'\'')
                }
            ),
              #widget.PulseVolume(
              #  font="FiraCode Bold",
              #  fontsize=20,
              #  foreground="ffffff",
              #  mouse_callbacks={
              #      'Button1': lazy.spawn("pavucontrol")  # Abre el control de volumen con clic izquierdo
              #  }
            #),
            widget.PulseVolume(
                fontsize=18,
                padding=15,
                #cardid="alsa_output.pci-0000_03_00.6.HiFi__Speaker__sink",
                #device="alsa_output.pci-0000_03_00.6.HiFi__Speaker__sink",
                #channel="HDMI1",
                channel="Master",
                foreground="bfbfbf",
                limit_max_volume=False,
                emoji=True,
                emoji_list=[' ','','',' '],
                mouse_callbacks={
                    'Button1': lazy.spawn('sh -c \'notify-send "Volumen" "$(pamixer --get-volume)"\''),
                    'Button3': lazy.spawn('sh -c \'"$(pamixer --toggle-mute)"\''),
                 }
            ),
            #widget.Wlan(),
            widget.BatteryIcon(
                theme_path=os.path.expanduser('~/.config/qtile/themes/icons/battery/'),
                scale=1.5,
                padding=3,
                mouse_callbacks={
                'Button1': lazy.spawn('sh -c \'notify-send "Batería" "$(acpi | cut -d, -f2)"\''),
                },
            ),
            #widget.Spacer(),
            #widget.QuickExit(
            #    default_text='',
            #    padding=5,
            #),
            #widget.Sep(),
            widget.Systray(icon_size = 20, background_color = "#ffffff"),
            widget.TextBox(" "),
        ],
        34,
        background="#00000000",
        margin=5,
        reserve=True,
    )








# Ruta del archivo de configuración
ip_file = os.path.expanduser("~/.config/qtile/themes/environment/ip.txt")

# Función para leer el estado desde el archivo
def read_ip():
    if os.path.exists(ip_file):
        with open(ip_file, "r") as file:
            return file.read().strip()
    return "192.168.1.100"  # Valor predeterminado

# Leer el entorno actual desde el archivo
ip = read_ip()








# Ruta del archivo de configuración
myip_file = os.path.expanduser("~/.config/qtile/themes/environment/myip.txt")
#myip = subprocess.run(["curl", "ipinfo.io/ip"])









# Ruta del archivo de configuración
targetip_file = os.path.expanduser("~/.config/qtile/themes/environment/targetip.txt")

# Función para leer el estado desde el archivo
def read_targetip():
    if os.path.exists(targetip_file):
        with open(targetip_file, "r") as file:
            return file.read().strip()
    return "192.168.1.100"  # Valor predeterminado

# Leer el entorno actual desde el archivo
targetip = read_targetip()








# Barra para Black Arch
def black_arch_bar():
    return bar.Bar(
        [
            widget.Image(
                filename="~/.config/qtile/themes/icons/Icono_Arch_rojo.png",
                margin_x=12,
                margin_y=4,
                mouse_callbacks = {
                'Button1': lazy.function(set_environment_to_arch),
                'Button2': lazy.function(show_program_menu, sex),
                'Button3': lazy.spawn("kitty --hold -e python3 /home/adrian/desktop/VSCode/HashArt/hash_art.py"),
                },
                #mouse_callbacksDict of mouse button press callback functions. Accepts functions and lazy calls.),
                scale=True,
                #width=20,
            ),
            widget.TextBox(' 󰣉 ', font="FiraCode Bold", fontsize="25"),
            widget.TextBox(ip, font="FiraCode Bold"),
            widget.TextBox(' 󰣉 ', font="FiraCode Bold", fontsize="25"),
            widget.TextBox(targetip, font="FiraCode Bold"),
            #Idea a implementar para el icono --> Como hay una función mouse_callback, puedo hacer que al darle al icono de arch, se ent>
            widget.Prompt(),
            widget.TextBox("", width=bar.STRETCH),
            widget.Clock(
                format="%d/%m/%Y %A %H:%M",
                fontsize=13,
                font='Helvetica '
                #foreground='#bfbfbf',
            ),
            widget.TextBox("", width=bar.STRETCH),
            #widget.Battery(format="{percent:2.0%}"),
            widget.CPUGraph(),
            widget.NetGraph(),
            widget.SwapGraph(),
            widget.HDDBusyGraph(),
            widget.HDDGraph(),
            widget.MemoryGraph(),
            widget.CheckUpdates(
                display_format='󰇚 {updates}  |',
                colour_have_updates='#bfbfbf',
                no_update_string='',
                fontsize=15,
                padding=8,
                mouse_callbacks={
                    'Button1': lazy.spawn('sh -c \'notify-send "Batería" "$(acpi | cut -d, -f2)"\''),
                 }
            ),
            #widget.Cmus(),
           widget.Wlan(
                interface='wlan0',
                ethernet_interface='enp3s0f3u1c2',
                fontsize=16,
                disconnected_message='',
                format=' ',
                foreground='#bfbfbf',
                padding=7,
                mouse_callbacks={
                    'Button1': lazy.spawn('sh -c \'notify-send "Batería" "$(acpi | cut -d, -f2)"\''),
                 }
            ),
            widget.Net(
                interface="enp3s0f3u1c2",
                fontsize=20,
                format='󰈀',
                foreground='#bfbfbf',
                use_bits=False,
                update_interval=1,
                padding=6,
                mouse_callbacks={
                    'Button1': lazy.spawn(
                        'notify-send "IP Address" "$(ip -4 addr show  | grep inet | awk \'{print $2}\' | cut -d\'/\' -f1)"'
                    )
                }
            ),
              #widget.PulseVolume(
              #  font="FiraCode Bold",
              #  fontsize=20,
              #  foreground="ffffff",
              #  mouse_callbacks={
              #      'Button1': lazy.spawn("pavucontrol")  # Abre el control de volumen con clic izquierdo
              #  }
            #),
            widget.PulseVolume(
                fontsize=18,
                padding=15,
                foreground="bfbfbf",
                limit_max_volume=True,
                emoji=True,
                emoji_list=[' ','','',' '],
                mouse_callbacks={
                    'Button1': lazy.spawn('sh -c \'notify-send "Volumen" "$(pamixer --get-volume)"\''),
                    'Button3': lazy.spawn('sh -c \'"$(pamixer --toggle-mute)"\''),
                 }
            ),
            #widget.Wlan(),
            widget.BatteryIcon(
                theme_path=os.path.expanduser('~/.config/qtile/themes/icons/battery/'),
                scale=1.5,
                padding=3,
                mouse_callbacks={
                'Button1': lazy.spawn('sh -c \'notify-send "Batería" "$(acpi | cut -d, -f2)"\''),
                },
            ),
            #widget.Spacer(),
            #widget.QuickExit(
            #    default_text='',
            #    padding=5,
            #),
            #widget.Sep(),
            widget.Systray(icon_size = 20, background_color = "#ffffff"),
            widget.TextBox(" "),
        ],
        34,
        background="#00000000",
        margin=5,
        reserve=True,
    )

# Asignación de la barra según el entorno actual
if current_environment == 'arch':
    screen_display = arch_bar()
else:
    screen_display = black_arch_bar()

screens = [
    Screen(
        top=screen_display
    ),
]
