import random


def gcd(a, b):
    """
    Calculate the Greatest Common Divisor (GCD) of a and b.
    """
    while b != 0:
        a, b = b, a % b
    return a


def xgcd(a, b):
    """
    Extended Euclidean Algorithm to find the multiplicative inverse.
    """
    x0, x1, y0, y1 = 1, 0, 0, 1
    while b != 0:
        q, a, b = a // b, b, a % b
        x0, x1 = x1, x0 - q * x1
        y0, y1 = y1, y0 - q * y1
    return x0


def is_prime(n, k=128):
    """
    Test if n is prime using Miller-Rabin primality test.
    """
    if n <= 1:
        return False
    # Find r, d such that n-1 = 2^r * d
    r, d = 0, n - 1
    while d % 2 == 0:
        r += 1
        d //= 2
    # Witness loop
    for _ in range(k):
        a = random.randrange(2, n - 1)
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True


def generate_prime_candidate(length):
    """
    Generate an odd integer randomly.
    """
    p = random.getrandbits(length)
    p |= (1 << length - 1) | 1
    return p


def generate_prime_number(length=1024):
    """
    Generate a prime number of given length.
    """
    p = 4
    while not is_prime(p, 128):
        p = generate_prime_candidate(length)
    return p


def generate_rsa_keys(length=1024):
    """
    Generate RSA public and private keys.
    """
    p = generate_prime_number(length // 2)
    q = generate_prime_number(length // 2)
    n = p * q
    phi = (p - 1) * (q - 1)

    e = 65537
    while gcd(e, phi) != 1:
        e = random.randrange(2, phi)

    d = xgcd(e, phi) % phi
    return ((e, n), (d, n))


def encrypt(public_key, plaintext):
    """
    Encrypt plaintext with the public key.
    """
    e, n = public_key
    ciphertext = [pow(ord(char), e, n) for char in plaintext]
    return ciphertext


def decrypt(private_key, ciphertext):
    """
    Decrypt ciphertext with the private key.
    """
    d, n = private_key
    plaintext = ''.join([chr(pow(char, d, n)) for char in ciphertext])
    return plaintext
