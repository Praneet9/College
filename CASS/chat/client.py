import socket
import rsa
from base64 import b64encode, b64decode
import sys

# taking port no as input
port = int(sys.argv[1])

# taking nickname of the user to be used in chat
client_nickname = sys.argv[2]

# connecting to the server
client = socket.socket()
client.connect(('localhost',port))

# taking input for the type of chat
choice = input('''
Select your choice of Chat!

1) Encrypted Chat
2) Digitally Signed
3) Both

Your choice = ''').encode()

# sending the choice of the client
client.send(choice)

# sending the nickname of the client
client.send(client_nickname.encode())

# receiving nickname of the server
server_nickname = client.recv(1024).decode()

# import keys of the client
public = rsa.importKey(client.recv(1024))
private = rsa.importKey(client.recv(1024))

# switch case based on user input
if int(choice) == 1:
    print('\nThe messages you send will be encrypted!\n')
    while True:
        # try block to catch the Keyboard Interrupt exception
        try:
            # input message to send to server
            msg = input(client_nickname + ": ").encode()
            encrypted = b64encode(rsa.encrypt(msg, public))

            # sending the encrypted message
            client.send(encrypted)
            # receiving the message from the server
            msge = client.recv(1024)
            # check if the user wants to quit the chat
            if msge.decode() == 'Quit':
                client.close()
                break
            else:
                print(server_nickname + ": " + str(rsa.decrypt(b64decode(msge), private).decode()))
        except KeyboardInterrupt:
            client.close()
            break
elif int(choice) == 2:
    print('\nThe messages you receive will be Digitally Signed!\n')
    # receiving the message from the server
    msg = client.recv(1024)

    # getting the signed text
    sign = client.recv(1024)

    # Verifying whether the plain msg and signed msg are same
    verify = rsa.verify(msg, b64decode(sign), public)

    if verify:
        print(server_nickname, "sent", msg.decode())
    else:
        print("You aren't authorised to check the message!")
    client.close()

elif int(choice) == 3:
    print('\nThe messages you send will be Encrypted as well as Digitally Signed!\n')

    # receiving the message from the server
    msg = client.recv(1024)

    # getting the signed text
    sign = client.recv(1024)

    # Verifying whether the plain msg and signed msg are same
    verify = rsa.verify(msg, b64decode(sign), public)

    if verify:

        while True:
            # try block to catch the Keyboard Interrupt exception
            try:
                # input message to send to server
                msg = input(client_nickname + ": ").encode()
                encrypted = b64encode(rsa.encrypt(msg, public))

                # sending the encrypted message
                client.send(encrypted)

                # receiving the message from the server
                msge = client.recv(1024)

                # check if the user wants to quit the chat
                if msge.decode() == 'Quit':
                    client.close()
                    break
                else:
                    # encrypted = client.recv(1024)
                    print(server_nickname + ": " + str(rsa.decrypt(b64decode(msge), private).decode()))
            except KeyboardInterrupt:
                client.close()
                break
    else:
        print("You aren't authorised to check the message!")
        client.close()
