import json
import socket
import threading
import sys
import os
import zipfile

#from client import order

HOST = "127.0.0.1"
PORT = 12700

list_client = []
list_Customer = {}


def accept_connections():
    global list_Customer
    readCustomer()

    while True:
        client, adr = ser.accept()
        print(f"Connected to {adr}")

        # Send menu
        with open("menu.json", 'r') as f:
            data = json.loads(f.read())
        # convert dict to strings
        menu = json.dumps(data)
        # Send menu
        client.sendall(menu.encode("utf8"))
        while True:
            mes = client.recv(1024).decode('utf8')
            if mes == "Received":
                print("Received successfully")
                break           
        
        # Send image
        # sendImage(client)
        print("start send menu")
        zip_name = "menu.zip"
        with zipfile.ZipFile(zip_name, 'w') as file:
            for j in ('banhcanh','coca','comsuon','hutieu','pepsi'):
                file.write('{}.jpg'.format(j))
                print('[+] {}.jpg is sent'.format(j))

        client.send(zip_name.encode())

        f = open(zip_name, 'rb')
        l = f.read()
        zipSize = str(len(l))
        client.send(zipSize.encode())

        client.sendall(l)

        f.close()
        os.remove(zip_name)
        print("stop send menu")
        #client.sendall("stop menu".encode('utf8'))
        while True:
            mes = client.recv(1024).decode('utf8')
            if mes == "Received":
                print("Received successfully")
                break  
        
        # Receive user name from client
        user_name = client.recv(1024).decode("utf8")
        list_client.append(client)
        print("User name:", user_name)

        print(f"{user_name} has come to order")

        threading.Thread(target=handle, args=(client, user_name,)).start()


def readCustomer():
    # Receive data of previous customers
    global list_Customer
    with open('cus.json', 'r') as f:
        data = json.loads(f.read())
    list_Customer = data.copy()


def sendImage(client):
    zip_name = "menu.zip"
    with zipfile.ZipFile(zip_name, 'w') as file:
        for j in ('banhcanh', 'coca', 'comsuon', 'hutieu', 'pepsi'):
            file.write('{}.jpg'.format(j))
            #print('[+] {}.jpg is sent'.format(j))

    client.send(zip_name.encode())

    f = open(zip_name, 'rb')
    l = f.read()
    client.sendall(l)
    # client.send("--done--".encode("utf8"))

    f.close()
    # os.remove(zip_name)

    return


def handle(client, nick):
    global list_Customer

    # Check if user has order before
    ordered = False
    for x in list_Customer:
        if nick == list_Customer[x]["name"]:
            ordered = True
            print(f"{nick} used to order.")
            client.sendall("ordered".encode('utf8'))
            user_info = json.dumps(list_Customer[x])
            client.sendall(user_info.encode('utf8'))

    if ordered == False:
        print(f"{nick} not order before")
        client.sendall("not ordered".encode('utf8'))

    # os.system("pause")
    # quit()

    # =========== receive customer's order
    mess = client.recv(1024).decode('utf8')
    data = client.recv(1024).decode('utf8')

    customer = json.loads(data)
    if mess == "update":
        # update customer["nick"]
        for x in list_Customer:
            if nick == list_Customer[x]["name"]:
                list_Customer[x] = customer
            pass
    else:
        # append customer["nick"]
        list_Customer.update({nick: customer})

    # Write to file customer.json
    data = json.dumps(list_Customer, indent=2)
    with open("cus.json", 'w') as file:
        file.write(data)

    list_client.remove(client)
    print(f"{nick} has left the store")
    client.close()


if __name__ == "__main__":
    ser = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ser.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    print("Socket created")

    try:
        ser.bind((HOST, PORT))
    except:
        print("Bind failed. Error: " + str(sys.exc_info()))
        sys.exit()

    ser.listen(6)   # Queue up to 5 requests
    accept_thread = threading.Thread(target=accept_connections)
    accept_thread.start()

