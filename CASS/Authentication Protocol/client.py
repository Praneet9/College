import socket

client_socket = socket.socket()
host = socket.gethostname()
port = 5000
client_socket.connect((host, port))

pwd = input("Enter password: ")
print("Sending token...")
client_socket.send(pwd.encode('utf-8'))
print("Receiving salted token...")
new_pwd = client_socket.recv(1024).decode('utf-8')
if (new_pwd == pwd + 'hello'):
	print("Connection Established")
	client_socket.send('True'.encode('utf-8'))
else:
	print("Connection broken")
	client_socket.send('False'.encode('utf-8'))