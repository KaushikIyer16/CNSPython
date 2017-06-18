import random
from random import randrange


def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

def primes_sieve(limit):
    limitn = limit+1
    not_prime = set()
    primes = []

    for i in range(2, limitn):
        if i in not_prime:
            continue

        for f in range(i*2, limitn, i):
            not_prime.add(f)

        primes.append(i)

    return primes


def multiplicative_inverse(e, phi):
    d = 0
    x1 = 0
    x2 = 1
    y1 = 1
    temp_phi = phi

    while e > 0:
        temp1 = temp_phi/e
        temp2 = temp_phi - temp1 * e
        temp_phi = e
        e = temp2

        x = x2- temp1* x1
        y = d - temp1 * y1

        x2 = x1
        x1 = x
        d = y1
        y1 = y

    if temp_phi == 1:
        return d + phi


def is_prime(num):
    if num == 2:
        return True
    if num < 2 or num % 2 == 0:
        return False
    for n in xrange(3, int(num**0.5)+2, 2):
        if num % n == 0:
            return False
    return True

def generate_keypair(p, q):
    if not (is_prime(p) and is_prime(q)):
        raise ValueError('Both numbers must be prime.')
    elif p == q:
        raise ValueError('p and q cannot be equal')

    n = p * q


    phi = (p-1) * (q-1)


    e = random.randrange(1, phi)


    g = gcd(e, phi)
    while g != 1:
        e = random.randrange(1, phi)
        g = gcd(e, phi)


    d = multiplicative_inverse(e, phi)


    return ((e, n), (d, n))

def encrypt(pk, plaintext):

    key, n = pk

    cipher = [(ord(char) ** key) % n for char in plaintext]

    return cipher

def decrypt(pk, ciphertext):

    key, n = pk

    plain = [chr((char ** key) % n) for char in ciphertext]

    return ''.join(plain)

def generatePQ():
    randList = primes_sieve(1000)
    pIndex = randrange(0,len(randList))
    qIndex = randrange(0,len(randList))
    p = randList[pIndex]
    q = randList[qIndex]
    return generate_keypair(p, q)


