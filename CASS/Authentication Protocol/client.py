import socket
import hashlib

client_socket = socket.socket()
host = socket.gethostname()
port = 7001
client_socket.connect((host, port))

pwd = input("Enter password: ")
# print(pwd)
hash_object_pwd = hashlib.sha1(pwd.encode('utf-8'))
pwd_hash = hash_object_pwd.hexdigest()
print("Sending token...")
client_socket.send(pwd.encode('utf-8'))
print("Receiving salted token...")
new_pwd = client_socket.recv(1024).decode('utf-8')
#print(new_pwd)
# hash_object = hashlib.sha1(new_pwd)
# new_pwd_hash = hash_object.hexdigest()
#print(pwd_hash,new_pwd_hash)
if (str(pwd_hash) == str(new_pwd)):
	print("Connection Established")
	client_socket.send('True'.encode('utf-8'))
else:
	print("Connection broken")
	client_socket.send('False'.encode('utf-8'))
