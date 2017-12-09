#!/usr/bin/env python3
import base64, os

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
    bytes = key.public_key().public_bytes(
        encoding=serialization.Encoding.DER,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    hash = Hash(SHA1(), backend=default_backend())
    hash.update(bytes[-24:])
    return base64.b32encode(hash.finalize()[:10]).lower()

OS_PATH = '/var/lib/tor/onion_service'
PRIV_KEY_PATH = os.path.join(OS_PATH, 'private_key')
HOSTNAME_PATH = os.path.join(OS_PATH, 'hostname')

if __name__ == '__main__':
    if os.path.exists(PRIV_KEY_PATH):
        with open(PRIV_KEY_PATH, 'rb') as file:
            privkey = serialization.load_pem_private_key(
                file.read(),
                password=None,
                backend=default_backend()
            )

    else:
        privkey = onion_keygen()
        with open(PRIV_KEY_PATH, 'w') as file:
            file.write(private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption
            ))


    hostname = onion_name(privkey)
    if not os.path.exists(HOSTNAME_PATH):
        with open(HOSTNAME_PATH, 'w') as file:
            file.write(hostname)
            file.write('\n')

    print('Onion service address', hostname)