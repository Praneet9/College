import socket
import pandas as pd
import time

# Server socket object
server_socket = socket.socket()
host = socket.gethostname()
port = 5000

# Bind to the socket
server_socket.bind((host, port))
server_socket.listen(1)

clientsocket, address = server_socket.accept()
print("Hello %s" %str(address))

dataframe = pd.read_csv('data.csv', index_col=0)
index,_ = address
# index = '127.0.0.2'
pwd = dataframe.loc[index, "Password"]
while True:
	print("Receiving token...")
	password = clientsocket.recv(1024).decode('utf-8')
	#time.sleep(100)
	print(password,pwd)
	if password == pwd:
		print("Correct Password")
	else:
		print("Incorrect Password")
		break
	new_pwd = pwd + 'hello'
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