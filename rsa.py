import random
import utils

def generate_keypair(length):
    if length <= 1:
        raise ValueError("Key length too small")

    p = utils.generate_prime(length)
    q = utils.generate_prime(length)
    while q == p:
        q = utils.generate_prime(length)
    n = p * q
    phi = (p - 1) * (q - 1)

    while True:
        e = random.randrange(3, phi, 2)
        if utils.modexp(e, 2, phi) == 1:
            # skip if the inverse of e mod phi is e
            continue
        if utils.gcd(e, phi) == 1:
            break

    d = utils.modinv(e, phi)
    return (e, n), (d, n)

def encrypt(message, public_key):
    return ""

def decrypt(message, private_key):
    return ""
