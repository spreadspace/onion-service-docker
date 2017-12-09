#!/bin/sh -e

# Fill-in environment variables in the torrc config file
cp /torrc /tmp/torrc
for var in TOR_CONTROL_PW ONION_HOST ONION_PORT; do
    eval val="\$$var"
    sed -i "s,{{ $var }},$val,g" /tmp/torrc
done

/keygen.py
touch /var/lib/tor/onion_service/onion_service_non_anonymous
exec /usr/bin/tor -f /tmp/torrc --RunAsDaemon 0
