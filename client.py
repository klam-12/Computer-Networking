import json
import socket
import threading
import os
import sys

lst_food = ["com suon",'mi y','hu tieu go','banh xeo','banh canh','pepsi','coca','tra da','sprite']
food_order = []
lst_quan = []
total = 0
status = False

def print_Menu(menu):
    print("-----------  MENU OF THE DAY -----------")

    for x in range(0,9):
        print('\t' + menu['foods'][x]['index'] + '. ' 
        + menu['foods'][x]['name'] + '\t' + str(menu['foods'][x]['price']) )
    
    print("-----------  ENJOY THE MEAL! -----------")

def print_Options():
    print("-----------  RUKI FOOD STORE -----------")
    print("\t1. View menu")
    print("\t2. Order")
    print("\t3. Payment")
    print("\t4. Exit")
    print("-----------  HAVE YOUR WISH  -----------")

def deleteClient(client):
    # inform server that this client has left
    client.sendall("quit".encode('utf8'))    
    client.close()

def account_numbers_checking():
    print("Enter your account numbers: ")
    account_numbers = input("Enter here: ")

    # Preprocessing
    account_numbers = account_numbers.strip(" ")

    # Length checking
    if len(account_numbers) != 10:
        return False

    # Char checking
    for char in account_numbers:
        try:
            int(char)
        except:
            return False

    return True


def payment():
    # Input Checking
    while True:
        # Check if user has no order.
        if total == 0:
            print("Your had no order before. Please order something to pay up")
            return False

        print(f"Total: {total}")
        print("Please Choose Payment Methods:")
        print("1. Cash Payment")
        print("2. Charge Card Payment")
        choice = input("Enter 1 or 2: ")
        mess = ""
        if choice == '1':
            break
        elif choice == '2':
            # Account numbers checking
            if account_numbers_checking() == False:
                print("Invalid account numbers. Please try again!")
                continue
            break
        else:
            print("Invalid choice. Please try again!")
            continue

    print("Successful payment")

    os.system("PAUSE")
#    sys.exit()
    return True

def checkFoodName_Quantity(idx, quan):
    if idx >= 0 and idx <= 8:
        if quan > 0:
            return True
        else:   
            return False
    return False


def order(menu):
    global total
    while True:
        foodIdx = input("Input the index of foods/drinks: ")
        quantity = input("Input the quantity: ")
        idx = int(foodIdx) - 1
        while checkFoodName_Quantity(idx,int(quantity)) == False:
            print("Wrong input. Try again!")
            foodIdx = input("Input the index of foods/drinks: ")
            quantity = input("Input the quantity: ")
            idx = int(foodIdx) - 1

        food_order.append(menu['foods'][idx]['name'])
        lst_quan.append(quantity)
        total += menu['foods'][idx]['price']*int(quantity)

        ans = input("Do you want to continue ordering?  ")
        if ans.lower() == 'no':
            break

def handle_Options(client, nick):
    # receive menu
    data = client.recv(1024).decode('utf8')
    # convert string to dict
    menu = json.loads(data)
    print_Options()

    status = False
    choice = input("Choose your option: ")
    while choice != '4':
        if choice == '1':
            print_Menu(menu)
        elif choice == '2':
            print_Menu(menu)
            order(menu)
            print("Total: " + str(total))
            print("Your foods have been installed successfully. Please come to pay up...")
        elif choice == '3':
            status = payment()
        else:
            print("Invalid options. Please try again!")
        print_Options()
        choice = input("Choose your option: ")
        
    print('**** Thank you for using our service ****')
    print('              See you again              ')
    
    #send data to server
    customer = {}
    customer.update({'name': nick})
    customer.update({'foods': food_order})
    customer.update({'quantity': lst_quan})
    customer.update({'total': total})
    if status == False:
        customer.update({'status': 'Not paid'})
    else:
        customer.update({'status': 'Paid'})

    data = json.dumps(customer)
    client.sendall(data.encode('utf8'))
    

def receive(client):
    mess = client.recv(1024).decode("utf8")
    print(mess)
    # input name
    nick = input("Please enter your name: ")
    client.sendall(nick.encode("utf8"))
    mess = client.recv(1024).decode('utf8')
    print(mess) # Let's order
#    os.system('cls')

    handle_Options(client,nick)
    
    client.close()

HOST = "127.0.0.1"
PORT = 12344

if __name__ == "__main__":
    client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    client.connect((HOST,PORT))
    receive_thread = threading.Thread(target=receive,args=(client,))
    receive_thread.start()