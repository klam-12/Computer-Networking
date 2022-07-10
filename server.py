import json
import socket
import threading
import sys

def accept_connections():
    while True:
        client, adr = ser.accept()
        print(f"Connected to {adr}")
        client.sendall("------ Welcome to Ruki Food Store ------".encode("utf8"))
        #receive name
        nick = client.recv(1024).decode("utf8")
        list_client.append(client)

        client.sendall("You are connected to our store. Let's order now".encode("utf8"))
        print(f"{nick} has come to order")

        threading.Thread(target=handle, args=(client,nick,)).start()

def readCustomer():
    # receive data of previous customers
    with open('cus.json','r') as f:
        data = json.loads(f.read())
    list_Customer = data.copy()

def handle(client, nick):
    readCustomer()

    # Send menu
    with open("menu.json",'r') as f:
        data = json.loads(f.read())
    #convert dict to strings
    menu = json.dumps(data)
    client.sendall(menu.encode("utf8"))
    
    # receive customer's order 
    data = client.recv(1024).decode('utf8')
    customer = json.loads(data)
    
    list_Customer.update({nick: customer})
    
    # write to file customer.json
    data = json.dumps(list_Customer, indent=2)
    with open("cus.json",'w') as file:
        file.write(data)

    list_client.remove(client)
    print(f"{nick} has left the store")
    client.close()

HOST = "127.0.0.1"
PORT = 12344

list_client = []
list_Customer = {}

if __name__ == "__main__":
    ser = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ser.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    print("Socket created")

    try:
        ser.bind((HOST,PORT))
    except:
        print("Bind failed. Error: " + str(sys.exc_info()))
        sys.exit()

    ser.listen(6)   # Queue up to 5 requests
    accept_thread = threading.Thread(target=accept_connections)
    accept_thread.start()

