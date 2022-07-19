import socket
import os
import zipfile

host = '127.0.0.1'
port = 1337
k = 3

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
print('[+] Client socket is created.')

s.connect((host, port))
print('[+] Socket is connected to {}'.format(host))

filename = s.recv(1024).decode()

f = open(filename, 'wb')
l = s.recv(1024)
while(l):
	f.write(l)
	l = s.recv(1024)
f.close()
print('[+] Received file ' + filename)

with zipfile.ZipFile(filename, 'r') as file:
	print('[+] Extracting files...')
	file.extractall()
	print('[+] Done')

os.remove(filename)
s.close()
