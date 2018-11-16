import socket

client_socket = socket.socket()
host = socket.gethostname()
port = 7000
client_socket.connect((host, port))

pwd = input("Enter password: ")
client_socket.send(pwd.encode('utf-8'))
