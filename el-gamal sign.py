import random


def gcd(x, y):
    while y:
        x, y = y, x % y
    return x


def gen_key(q):
    key = random.randint(pow(10, 20), q)
    while gcd(q, key) != 1:
        key = random.randint(pow(10, 20), q)

    return key


def power(a, b, c):
    x = 1
    y = a

    while b > 0:
        if b % 2 != 0:
            x = (x * y) % c
        y = (y * y) % c
        b = int(b / 2)

    return x % c


def phi(n):
    result = n
    for i in range(2, n):
        if i * i > n:
            break
        if n % i == 0:
            while n % i == 0:
                n /= i
            result -= int(result / i)
    if n > 1:
        result -= int(result / n)
    return result


def encrypt(msg, p, g):
    m = hash(msg)
    m = m % (p - 1)
    print(m)
    x = random.randint(1, p)
    y = power(g, x, p)
    k = power(x, phi(p) - 1, p)
    r = (m * power(g, k, p)) % p
    return r, y


def verify(msg, r, p, g, y):
    if not (0 < r < p and 0 < y < p):
        print("wrong sign")
    m = hash(msg)
    m = m % (p - 1)
    print(m)
    if (r * y % p == m * g):
        print("verified")


msg = 'love you so much'
print("message: ", msg)

p = random.randint(pow(10, 20), pow(10, 50))
g = random.randint(2, p)

r, y = encrypt(msg, p, g)
print('')

verify(msg, r, p, g, y)
