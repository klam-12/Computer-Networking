import socket
import sys
import zipfile
import os

host = '127.0.0.1'
port = 1337
zip_name = "menu.zip"

ss = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
print('[+] Server socket is created.')

ss.bind((host, port))
print('[+] Socket is binded to {}'.format(port))

ss.listen(5)
print('[+] Waiting for connection...')

con, addr = ss.accept()
print('[+] Got connection from {}'.format(addr[0]))

with zipfile.ZipFile(zip_name, 'w') as file:
	for j in ('banhcanh','coca','comsuon','hutieu','pepsi'):
		file.write('{}.jpg'.format(j))
		print('[+] {}.jpg is sent'.format(j))

con.send(zip_name.encode())

f = open(zip_name, 'rb')
l = f.read()
con.sendall(l)

f.close()
os.remove(zip_name)

con.close()
ss.close()