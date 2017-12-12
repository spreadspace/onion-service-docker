# onion-service-docker
A Docker container for exposing applications as Tor onion services.

**WARNING**: This container makes **non-anonymous**, single-hop onion services.

https://hub.docker.com/r/spreadspace/onion-service/

## Usage

Pass the `ONION_HOST` and `ONION_PORT` environment variables (the host and port
that should be exposed as an onion service) when starting the container.

Optionally, you can pass a hashed password as `TOR_CONTROL_PW` to restrict
access to little-t tor's control port.
