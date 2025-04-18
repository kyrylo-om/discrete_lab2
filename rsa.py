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
    e, n = public_key

    N = 1
    while int("25" * N) < n:
        N += 1

    ord_message = []
    block = ""
    message = message.lower()
    for char in message:
        block += f"{ord(char) - 97:0{2}}"
        if len(block) >= 2 * N:
            ord_message.append(block)
            block = ""
    if block != "":
        while len(block) < 2 * N:
            # 99 - фіктивний символ
            block += "99"
        ord_message.append(block)

    return " ".join([str(utils.modexp(int(block), e, n)) for block in ord_message])

def decrypt(message, private_key):
    return ""
