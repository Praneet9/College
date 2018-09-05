import socket
import rsa
from base64 import b64encode, b64decode
import sys

port = int(sys.argv[1])
server_nickname = sys.argv[2]

public, private = rsa.newkeys()
public_test, private_test = rsa.newkeys()

server = socket.socket()
server.bind(('localhost',port))
server.listen(10)

conn, address = server.accept()

# receiving the choice of the client
choice = int(conn.recv(1024))

# receiving the nickname of the client
client_nickname = conn.recv(1024).decode()

# sending nickname of the server
conn.send(server_nickname.encode())

#send public key
conn.send(public.exportKey())
conn.send(private.exportKey())

if choice == 1:
    print('\nThe messages you send will be encrypted!\n')
    while True:
        try:
            # Receive encrypted message
            msg = conn.recv(1024)
            print(client_nickname + ": " + str(rsa.decrypt(b64decode(msg), private).decode()))
            msge = input(server_nickname + ": ").encode()
            if msge == b'Quit':
                conn.send(msge)
                conn.close()
                break
            else:
                encrypted = b64encode(rsa.encrypt(msge, public))
                conn.send(encrypted)
        except KeyboardInterrupt:
            client.close()
            break
elif choice == 2:
    print('\nThe messages you send will be Digitally Signed!\n')

    # Sending message
    msg = input(server_nickname + ": ").encode()
    conn.send(msg)

    # Sending signature
    signature = b64encode(rsa.sign(msg, private))
    conn.send(signature)
elif choice == 3:
    print('\nThe messages you send will be Encrypted as well as Digitally Signed!\n')
    msg = input(server_nickname + ": ").encode()
    conn.send(msg)

    # Sending signature
    signature = b64encode(rsa.sign(msg, private))
    conn.send(signature)
    while True:
        try:
            # Receive encrypted message
            msg = conn.recv(1024)
            print(client_nickname + ": " + str(rsa.decrypt(b64decode(msg), private).decode()))
            msge = input(server_nickname + ": ").encode()
            if msge == b'Quit':
                conn.send(msge)
                conn.close()
                break
            else:
                encrypted = b64encode(rsa.encrypt(msge, public))
                conn.send(encrypted)
        except KeyboardInterrupt:
            client.close()
            break
else:
    conn.close()
