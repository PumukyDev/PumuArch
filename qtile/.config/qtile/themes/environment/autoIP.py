#!/bin/bash

# Obtén la primera puerta de enlace de la interfaz Ethernet
GATEWAY=$(ip route show dev eth0 | grep default | awk '{print $3}' | head -n 1)

if [[ "$GATEWAY" == "192.168.112.1" ]]; then
    # Si estás en el colegio, cambia a IP estática
    nmcli connection modify "Wired connection 1" ipv4.addresses "192.168.112.140/24"
    nmcli connection modify "Wired connection 1" ipv4.gateway "192.168.112.1"
    nmcli connection modify "Wired connection 1" ipv4.dns "8.8.8.8 8.8.4.4"
    nmcli connection modify "Wired connection 1" ipv4.method manual
else
    # Si no estás en el colegio, usa IP dinámica
    nmcli connection modify "Wired connection 1" ipv4.method auto
fi

# Reinicia la conexión Ethernet para aplicar los cambios
nmcli connection down "Wired connection 1"
nmcli connection up "Wired connection 1"
