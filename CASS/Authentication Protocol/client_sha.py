import socket
import hashlib

client_socket = socket.socket()
host = socket.gethostname()
port = 6000
client_socket.connect((host, port))

# pwd = input("Enter password")

hash_object = hashlib.sha1(b'1234354346')
hex_dig = hash_object.hexdigest()
print(hex_dig)
client_socket.send(str(hex_dig))