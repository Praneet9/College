import numpy

def _housekeeping(input_string, matrix_size):

    garbage = matrix_size - len(input_string) % matrix_size
    input_string = input_string + '$'*garbage

    return input_string

def blockCipher(input_string):

    k = int(input("Enter key size: "))
    matrix_size = k ** 2

    input_string = _housekeeping(input_string, matrix_size)
    matrix = []
    start = 0

    for i in range(start, len(input_string), matrix_size):
        temp = []
        for n in range(k):
            temp.append(list(input_string[start:start + k]))
            start = start + k
        matrix.append(temp)

    test = []

    for i in range(len(matrix)):
        test.append(numpy.transpose(matrix[i]))
    outputtext = ""
    for j in range(len(matrix)):
        for i in test[j]:
            outputtext = outputtext + "".join(list(i))

    return outputtext

select_type = input("Press e for Encryption and d for Decryption: ")

if select_type is "e":

    text = input("Enter text to Encrypt: ")

    outputtext = blockCipher(text)
    print("Before Encryption: " + text + "\nAfter Encryption: " + outputtext)

elif select_type is "d":

    text = input("Enter text to Decrypt: ")

    outputtext = blockCipher(text).replace('$','')
    print("Before Decryption: " + text + "\nAfter Decryption: " + outputtext)

else:

    print("Select valid type")
