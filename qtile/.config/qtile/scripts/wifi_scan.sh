#!/bin/bash

# Intervalo de actualización en segundos
INTERVAL=5

while true; do
    clear  # Limpia la pantalla
    echo "Escaneando redes WiFi..."
    nmcli device wifi list  # Lista las redes WiFi disponibles
    echo ""
    echo "Actualizando en $INTERVAL segundos. Presiona Ctrl+C para salir."
    sleep $INTERVAL  # Espera el intervalo definido antes de actualizar
done
