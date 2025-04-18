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

    N = utils.calculate_max_N(n)

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
    # Декодуємо кожен блок за допомогою приватного ключа
    blocks = message.strip().split()
    decrypted_blocks = [str(decrypt_block(int(block), private_key)) for block in blocks]

    # Дізнаємось довжину блоку: N * 2 (бо кожна літера — 2 цифри)
    block_length = calculate_max_N() * 2

    # Заповнюємо нулями зліва до block_length
    numeric_string = ''.join(block.zfill(block_length) for block in decrypted_blocks)

    # Декодуємо повідомлення по 2 цифри
    decoded_message = ""
    for i in range(0, len(numeric_string), 2):
        code = int(numeric_string[i:i+2])
        if code < 26:  # 0-25 для A-Z
            decoded_message += chr(ord('A') + code)
        # Інакше — фіктивний символ, пропускаємо

    return decoded_message
