#!/bin/bash

GATEWAY=$(ip route | grep default | awk '{print $3}')

if [[ "$GATEWAY" == "10.112.0.2" ]]; then
    # Configura la IP del colegio
    ip addr flush dev eth0
    ip addr add 10.112.40.1/16 dev eth0
    ip route add default via 10.112.0.2
elif [[ "$GATEWAY" == "192.168.1.1" ]]; then
    # Configura la IP de casa
    ip addr flush dev eth0
    ip addr add 192.168.1.37/24 dev eth0
    ip route add default via 192.168.1.1
fi

