import random

p = 17
q = 23
n, k, e, d, lam = 0, 0, 0, 0, 0


def is_prime(x):
    count = 0
    for i in range(int(x/2)):
        if x % (i+1) == 0:
            count = count+1
    return count == 1


def generate_random_prime():
    global message
    x = random.randint(20000, 100000)
    while not is_prime(x):
        x = random.randint(20000, 100000)
    return x


def is_strong(num):
    last = num - 1
    next = num + 1
    while not is_prime(next):
        next += 1
    while not is_prime(last):
        last -= 1
    avg = (last + next) / 2
    if num > avg:
        return True
    return False


def randomize_pqk():
    global p, q, k, n
    p = generate_random_prime()
    print("random p: ")
    print(p)
    # while not is_strong(p):
    #    p = generate_random_prime()
    print("random q: ")
    q = generate_random_prime()
    print(q)
    # while abs(p-q) < 20000 or (not is_strong(q)):
    while abs(p - q) < 20000:
        print(q)
        q = generate_random_prime()
    n = p * q
    k = random.randint(10000, n)
    print("random k: ")
    print(k)
    while k == p or k == q or (n % k == 0):
        k = random.randint(10000, n)
        print(k)


def gcd(x, y):
    while y:
        x, y = y, x % y
    return x


def lcm(x, y):
    return (x*y)//gcd(x, y)


def ex_gcd(a, b):
    if a == 0:
        return b, 0, 1
    else:
        gcd_var, x, y = ex_gcd(b % a, a)
        return gcd_var, y - (b // a) * x, x


def power(x, y):
    temp = 0
    if y == 0:
        return 1
    temp = power(x, int(y / 2))
    if y % 2 == 0:
        return (temp * temp) % n
    else:
        return (x * temp * temp) % n


def randomize_all():
    global n, d, e, lam
    randomize_pqk()
    n = p * q
    print("n: ")
    print(n)
    print("lam: ")
    lam = lcm(p - 1, q - 1)
    print(lam)
    print("e: ")
    e = random.randint(2, lam)
    print(e)
    while gcd(e, lam) != 1:
        e = random.randint(2, lam)
        print(e)
    gcd_arr = ex_gcd(e, lam)
    d = gcd_arr[1]
    print("d: ")
    d = (d % lam + lam) % lam
    print(d)


def encrypt_rsa(message):
    global n, e
    cypher_text = power(message, e) % n
    return cypher_text


def decrypt_rsa(cypher_text):
    global d
    msg = int(power(int(cypher_text), int(d))) % int(n)
    return msg


def encrypt(message):
    arr = []
    for el in message:
        arr.append(encrypt_rsa(ord(el)))
    result = "".join([str(elem) + ' ' for elem in arr])
    return result


def decrypt(cypher):
    arr = cypher.split()
    string = ""
    for el in arr:
        string += chr(decrypt_rsa(int(el)))
    return string


def convert_to_int(text):
    string = ""
    for char in text:
        string += str(ord(char))
    return int(string)


f = open("message.txt", "r")
message = f.read()
randomize_all()
cypher = encrypt(message)
print("\nmessage: ")
print(message)
print("Cypher text:")
print(cypher)
m = decrypt(cypher)
print("decrypted:")
print(m)

f = open("cypher.txt", "w")
f.write(str(cypher))
f.close()
