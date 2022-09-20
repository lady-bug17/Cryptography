def encode_caesar(text, slide):
    cypher = ""
    for i in range(len(text)):
        if 'a' <= text[i] <= 'z':
            cypher += chr((ord(text[i]) - ord('a') + slide) % 26 + ord('a'))
        elif 'A' <= text[i] <= 'Z':
            cypher += chr((ord(text[i]) - ord('A') + slide) % 26 + ord('A'))
        else:
            cypher += text[i]
    return cypher


def decode_caesar(cypher, slide):
    return encode_caesar(cypher, -slide)


def encode_polybius(text, slide):
    if slide % 2 == 0:
        slide -= 1
    cypher = ""
    x_es = ""
    y_es = ""
    for i in range(len(text)):
        if 'a' <= text[i] <= 'z':
            n = ord(text[i]) - ord('a') + 1
            if text[i] == 'z':
                i, j = 5, 5
            else:
                i = int((n + 4) / 5) # ceil(a/b) = (a+b-1)/b
                j = n % 5
            x_es += str(j)
            y_es += str(i)
        elif 'A' <= text[i] <= 'Z':
            n = ord(text[i]) - ord('A') + 1
            if text[i] == 'Z':
                i, j = 5, 5
            else:
                i = int((n + 4) / 5)
                j = 5
            x_es += str(j)
            y_es += str(i)

    primary_cypher = x_es + y_es
    slided_cypher = primary_cypher[slide:] + primary_cypher[:slide]
    for i in range(0, len(slided_cypher), 2):
        cypher += chr(5 * (int(slided_cypher[i]) - 1) + int(slided_cypher[i+1]) + ord('a')-1)
    return cypher


def decode_polybius(cypher, slide):
    slided_cypher = ""
    for i in range(len(cypher)):
        if 'a' <= cypher[i] <= 'z':
            n = ord(cypher[i]) - ord('a') + 1
            if cypher[i] == 'z':
                i, j = 5, 5
            elif n % 5 != 0:
                i = int(n / 5) + 1
                j = n % 5
            else:
                i = int(n / 5)
                j = 5
            slided_cypher += str(i) + str(j)
        elif 'A' <= cypher[i] <= 'Z':
            n = ord(cypher[i]) - ord('A') + 1
            if cypher[i] == 'Z':
                i, j = 5, 5
            elif n % 5 != 0:
                i = int(n / 5) + 1
                j = n % 5
            else:
                i = int(n / 5)
                j = 5
            slided_cypher += str(i) + str(j)
    primary_cypher = slided_cypher[-slide:] + slided_cypher[:-slide]
    x_es = primary_cypher[:int(len(primary_cypher)/2)]
    y_es = primary_cypher[int(len(primary_cypher)/2):]
    text = ""
    for i in range(len(x_es)):
        text += chr((int(y_es[i])-1)*5 + int(x_es[i]) + ord('a') - 1)
    return text


def encode_gronsweld(text, key):
    key *= (len(text) // len(key)) + 1
    print(key)
    cypher = ""
    for i in range(len(text)):
        if 'a' <= text[i] <= 'z':
            if ord(text[i]) + int(key[i]) <= ord('z'):
                cypher += chr(ord(text[i])+int(key[i]))
            else:
                cypher += chr(ord(text[i])+int(key[i])-ord('z'))
        elif 'A' <= text[i] <= 'Z':
            if ord(text[i]) + int(key[i]) <= ord('Z'):
                cypher += chr(ord(text[i])+int(key[i]))
            else:
                cypher += chr(ord(text[i])+int(key[i])-ord('Z'))
        else:
            cypher += text[i]
    return cypher


def decode_gronsweld(text, key):
    key *= (len(text) // len(key)) + 1
    print(key)
    cypher = ""
    for i in range(len(text)):
        if 'a' <= text[i] <= 'z':
            if ord(text[i]) - int(key[i]) >= ord('a'):
                cypher += chr(ord(text[i]) - int(key[i]))
            else:
                cypher += chr(ord(text[i]) - int(key[i]) + ord('z'))
        elif 'A' <= text[i] <= 'Z':
            if ord(text[i]) - int(key[i]) >= ord('A'):
                cypher += chr(ord(text[i]) - int(key[i]))
            else:
                cypher += chr(ord(text[i]) - int(key[i]) + ord('Z'))
        else:
            cypher += text[i]
    return cypher


def create_matrix(key):
    used = [False] * 25
    matrix = [[None for i in range(5)] for j in range(5)]
    iter = 0
    for i in key:
        n = ord(i) - ord('a')
        if not used[n]:
            matrix[iter // 5][iter % 5] = i
            iter += 1
            used[n] = True
    for i in range(25):
        if not used[i]:
            matrix[iter // 5][iter % 5] = chr(ord('a') + i)
            iter += 1
    return matrix


def encode_playfair(txt, key, decode=1):
    matrix = create_matrix(key)
    text = txt.lower()
    indices = {}
    for i in range(5):
        for j in range(5):
            indices[matrix[i][j]] = [i, j]
    accumulator = ""
    for i in text:
        if 'a' <= i <= 'y':
            if len(accumulator) % 2 == 1 and accumulator[-1] == i:
                accumulator += 'x'
            accumulator += i
    if len(accumulator) % 2 == 1:
        accumulator += 'x'
    cypher = ""
    for i in range(0, len(accumulator), 2):
        x1 = indices.get(accumulator[i])
        x2 = indices.get(accumulator[i + 1])
        if x1[0] == x2[0]:
            cypher += matrix[x1[0]][(x1[1]+5+decode) % 5]
            cypher += matrix[x2[0]][(x2[1]+5+decode) % 5]
        elif x1[1] == x2[1]:
            cypher += matrix[(x1[0]+5+decode) % 5][x1[1]]
            cypher += matrix[(x2[0]+5+decode) % 5][x2[1]]
        else:
            cypher += matrix[x1[0]][x2[1]]
            cypher += matrix[x2[0]][x1[1]]
    pers = 0
    cypher_text = ""
    for i in range(len(text)):
        if 'a' <= text[i] <= 'y':
            if accumulator[i+pers] == text[i]:
                cypher_text += cypher[i+pers]
            else:
                cypher_text += cypher[i+pers]
                pers += 1
                cypher_text += cypher[i+pers]
        else:
            cypher_text += text[i]
            pers -= 1
    if len(text) + pers < len(cypher):
        cypher_text += cypher[-1]
    return cypher_text







#slide = int(input())

text_file = open("text.txt")
caesar_file = open("encodeCaesar", "w")
polybius_file = open("encodePolybius", "w")
gronsweld_file = open("encodeGronsweld", "w")
playfair_file = open("encodePlayfair", "w")

text = text_file.read()

playfair_key = "sadcat"
caesar_key = -1
gronsweld_key = "2015"
polybius_key = 1

cypher = encode_playfair(text, playfair_key)
playfair_file.write(cypher)
print("Playfair decode: \n")
print(encode_playfair(cypher, playfair_key, -1))
cypher = encode_caesar(text, caesar_key)
caesar_file.write(cypher)
print("Caesar decode: \n")
print(decode_caesar(cypher, caesar_key))
cypher = encode_polybius(text, polybius_key)
polybius_file.write(cypher)
print("Polybius decode: \n")
print(decode_polybius(cypher, polybius_key))
cypher = encode_gronsweld(text, gronsweld_key)
gronsweld_file.write(cypher)
print("Gronsweld decode: \n")
print(decode_gronsweld(cypher, gronsweld_key))



#caesar_cypher = encode_caesar(text, slide)
#polybius_cypher = encode_polybius(text, slide)

#code = decode_polybius(polybius_cypher, slide)
#print(code)

#polybius_file.write(polybius_cypher)
#caesar_file.write(str(caesar_cypher))
#caesar_file.close()
