#!/bin/sh -e

# Fill-in environment variables in the torrc config file
cp /torrc /tmp/torrc
for var in TOR_CONTROL_PW ONION_HOST ONION_PORT; do
    eval val="\$$var"
    sed -i "s,{{ $var }},$val,g" /tmp/torrc
done


# If the onion service key already exists, displya the hostname
if [ -f /var/lib/tor/onion_service/hostname ]; then
    echo -n 'Onion service address: '
    cat /var/lib/tor/onion_service/hostname
fi


exec /usr/bin/tor -f /tmp/torrc --RunAsDaemon 0
