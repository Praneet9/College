import socket
import pandas as pd
import time
import hashlib
# Server socket object
server_socket = socket.socket()
host = socket.gethostname()
port = 7001

# Bind to the socket
server_socket.bind((host, port))
server_socket.listen(1)

clientsocket, address = server_socket.accept()
print("Hello %s" %str(address))

dataframe = pd.read_csv('data.csv', index_col=0)
index,_ = address
# index = '127.0.0.2'
pwd = dataframe.loc[index, "Password"]

def encrypt(new_pwd_here):
	hash_object_pwd = hashlib.sha1(new_pwd_here.encode('utf-8'))
	pwd_hash = hash_object_pwd.hexdigest()
	return pwd_hash

while True:
	print("Receiving token...")
	password = clientsocket.recv(1024).decode('utf-8')
	#time.sleep(100)
	#print(password,pwd)
	if password == pwd:
		print("Correct Password")
	else:
		print("Incorrect Password")
		break
	new_pwd = str(encrypt(pwd))
	print("Sending salted token...")
	clientsocket.send(new_pwd.encode('utf-8'))
	confirmation = clientsocket.recv(1024).decode('utf-8')
	if confirmation == 'True':
		print("Connection Established")
		break
	else:
		print("Connection Broken")
		break
clientsocket.close()
