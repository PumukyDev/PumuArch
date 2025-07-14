#!/bin/sh

#Configuración teclado español
setxkbmap es &

#iconos del sistema

#udiskie -t &

nm-applet &

volumeicon &

cbatticon -u 5 &

#nitrogen --restore &

greenclip --daemon &

picom --daemon &

# Obtener la información de las pantallas con xrandr
connected_outputs=$(xrandr | grep " connected")

# Verificar si hay pantallas conectadas
if [ -z "$connected_outputs" ]; then
    # No hay pantallas conectadas
    /home/Adrian/.screenlayout/resolucion.sh
else
    # Hay al menos una pantalla conectada
    while read -r line; do
        output=$(echo "$line" | awk '{print $1}')
        resolution=$(echo "$line" | awk '{print $3}')

        case $output in
            "HDMI-1") 
            /home/Adrian/.screenlayout/resolucion_casa_lg.sh
                #if [ "$resolution" == "1600x900+1920+0" ]; then
                    # Pantalla de casa
                 #   /home/Adrian/.screenlayout/resolucion_casa.sh
                #elif [ "$resolution" == "OtraResolucion" ]; then
                    # Pantalla del colegio
                 #   /ruta/completa/a/resolucion_colegio.sh
                #fi
                ;;
            # Puedes agregar más casos según sea necesario para otras pantallas
        esac
    done <<< "$connected_outputs"
fi


~/.config/qtile/scripts/save_interface.sh &

~/.fehbg &