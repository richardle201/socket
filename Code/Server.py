import socket
import os
import threading
import hashlib


# Create Socket (TCP) Connection
ServerSocket = socket.socket(family = socket.AF_INET, type = socket.SOCK_STREAM) 
host = socket.gethostname()
port = 1233
ThreadCount = 0
try:
    ServerSocket.bind((host, port))
except socket.error as e:
    print(str(e))

print('Waitiing for a Connection..')
ServerSocket.listen(5)
HashTable = {}

# Function : For each client 
def threaded_client(connection):
    while True:
        connection.send(str.encode('ENTER USERNAME : ')) # Request Username
        name = connection.recv(2048)
        connection.send(str.encode('ENTER PASSWORD : ')) # Request Password
        password = connection.recv(2048)
        password = password.decode()
        name = name.decode()
        #Ma hoa password
        password=hashlib.sha256(str.encode(password)).hexdigest() # Password hash using SHA256
# REGISTERATION PHASE   
# If new user,  regiter in Hashtable Dictionary  
        if name not in HashTable:
            HashTable[name]=password
            connection.send(str.encode('Registeration Successful')) 
            print('Registered : ',name)
            print("{:<8} {:<20}".format('USER','PASSWORD'))
            for k, v in HashTable.items():
                label, num = k,v
                print("{:<8} {:<20}".format(label, num))
            print("-------------------------------------------")
            break
        else:
# If already existing user, check if the entered password is correct
            connection.send(str.encode('Username already existed'))
            print('Sign up failed')
    while True:
        break
    connection.close()

while True:
    Client, address = ServerSocket.accept()
    client_handler = threading.Thread(
        target=threaded_client,
        args=(Client,)  
    )
    client_handler.start()
    ThreadCount += 1
    print('Connection Request: ' + str(ThreadCount))
ServerSocket.close()
