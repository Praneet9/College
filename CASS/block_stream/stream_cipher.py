k = 3

outputtext = ""

def encrypt(c):

    return (pooldict[c] + k) % 26

def decrypt(c):

    return ((pooldict[c] + 26) - k) % 26

pooldict = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5,
            'g': 6, 'h': 7, 'i': 8, 'j': 9, 'k': 10,
            'l': 11, 'm': 12, 'n': 13, 'o': 14, 'p': 15,
            'q': 16, 'r': 17, 's': 18, 't': 19, 'u': 20,
            'v': 21, 'w': 22, 'x': 23, 'y': 24, 'z': 25}

poollist = sorted(list(pooldict.keys()))

select_type = input("Press e for Encryption and d for Decryption: ")

if select_type is "e":

    text = input("Enter text: ")
    text = text.lower()

    for character in text:
        if character in pooldict:
            outputtext = outputtext + poollist[encrypt(character)]
        else:
            outputtext = outputtext + character
    print("Before Encryption: " + text + "\nAfter Encryption: " + outputtext)

elif select_type is "d":

    text = input("Enter text: ")
    text = text.lower()

    for character in text:
        if character in pooldict:
            outputtext = outputtext + poollist[decrypt(character)]
        else:
            outputtext = outputtext + character
    print("Before Decryption: " + text + "\nAfter Decryption: " + outputtext)

else:

    print("Select valid type")
