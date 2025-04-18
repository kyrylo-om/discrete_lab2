import random
import math

def calculate_hash(message):
    # It is important for the hash to be exactly 64 symbols long.

    return "0"*64

def is_prime(n):
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False

    # all prime numbers can be expressed as 6k +- 1 so we check them
    i = 5
    while i ** 2 <= n:
        # i will always equal 6k - 1 so we check it and also i + 2
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

def generate_prime(length):
    # check for prime all numbers in the form of 6k +- 1
    # the larger the length the larger the returned number
    while True:
        k = random.randrange(2**(length - 1), 2**length)

        if is_prime(6 * k - 1):
            return 6 * k - 1
        elif is_prime(6 * k + 1):
            return 6 * k + 1

def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

def modinv(a, n):
    original_n = n
    x0, x1 = 0, 1

    while a > 1:
        q = a // n
        a, n = n, a % n
        x0, x1 = x1 - q * x0, x0

    return x1 % original_n

def modexp(a, b, m):
    result = 1
    base = a % m
    exponent = b

    while exponent > 0:
        if exponent % 2 == 1:
            result = (result * base) % m
        exponent //= 2
        base = (base * base) % m

    return result

def calculate_max_N(n):
    N = 1
    while int("25" * N) < n:
        N += 1
    return N
