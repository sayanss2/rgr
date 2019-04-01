#! /usr/bin/python3
import socket
import getpass

user = str(getpass.getuser())
out = 'error'
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
	sock.sendto(user.encode('utf-8'), ('127.0.0.1',40069))
	date, addr = sock.recvfrom(1024)
	if date:
		out = date.decode('utf-8')
print(user + ", Ваш вариант № " + out)