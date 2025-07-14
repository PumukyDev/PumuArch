#!/bin/bash

# Esperar unos segundos para permitir que la interfaz se active
#sleep 1

# Detectar interfaz Ethernet sin los dos puntos al final
INTERFACE=$(ip link | grep -E 'enp|eth' | grep -oE '^[0-9]+: [^ ]+' | awk '{print $2}' | sed 's/://')

# Guardar interfaz en un archivo
echo $INTERFACE > /home/adrian/.config/qtile/themes/environment/current_interface.txt

#Necesitamos que ele ejecute adrian porque si no lo va aa hacer root y enetonces no va a funcionar
 su adrian -c "/usr/bin/qtile cmd-obj -o cmd -f reload_config"