#!/usr/bin/env python3

from base64 import b32encode
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.hashes import Hash, SHA1


def onion_keygen():
    return rsa.generate_private_key(
        public_exponent=65537,
        key_size=1024,
        backend=default_backend()
    )


def onion_name(key):
    pub_bytes = key.public_key().public_bytes(
        encoding=serialization.Encoding.DER,
        format=serialization.PublicFormat.PKCS1
    )
    hash = Hash(SHA1(), backend=default_backend())
    hash.update(pub_bytes)
    return b32encode(hash.finalize()[:10]).lower() + b'.onion'


if __name__ == '__main__':
    import os
    OS_PATH = '/var/lib/tor/onion_service'
    PRIV_KEY_PATH = os.path.join(OS_PATH, 'private_key')
    HOSTNAME_PATH = os.path.join(OS_PATH, 'hostname')

    if os.path.exists(PRIV_KEY_PATH):
        with open(PRIV_KEY_PATH, 'rb') as file:
            privkey = serialization.load_pem_private_key(
                file.read(),
                password=None,
                backend=default_backend()
            )

    else:
        privkey = onion_keygen()
        with open(PRIV_KEY_PATH, 'wb') as file:
            file.write(privkey.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption
            ))

    hostname = onion_name(privkey)
    if not os.path.exists(HOSTNAME_PATH):
        with open(HOSTNAME_PATH, 'wb') as file:
            file.write(hostname)
            file.write(b'\n')

    print('Onion service address:', hostname)
