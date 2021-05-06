import socket
import os
import threading
import json


# Create Socket (TCP) Connection
ServerSocket = socket.socket(family = socket.AF_INET, type = socket.SOCK_STREAM) 
host = '127.0.0.1'
port = 1233
ThreadCount = 0
try:
    ServerSocket.bind((host, port))
except socket.error as e:
    print(str(e))

print('Waitiing for a Connection..')
ServerSocket.listen(5)

userdata = {}
userdata['account'] = []
with open('userdata.json','w') as f: 
		json.dump(userdata, f, indent=2) 


def write_json(data, filename='userdata.json'): 
	with open(filename,'w') as f: 
		json.dump(data, f, indent=2) 

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
        #password=hashlib.sha256(str.encode(password)).hexdigest() # Password hash using SHA256
# REGISTERATION PHASE   
# If new user,  register in Hashtable Dictionary
        with open('userdata.json','r') as json_file:
            userdata = json.load(json_file)

        check_exist = any(name in d['username'] for d in userdata['account'])

        if check_exist == False:
        #if name not in userdata['account']:
            with open('userdata.json','r') as json_file: 
                data = json.load(json_file) 
                temp = data['account'] 
                # python object to be appended 
                new_user = {'username': name, 'password':password}
                temp.append(new_user)
                
                write_json(data) 
                connection.send(str.encode('Registeration Successful')) 
                print('Registered : ',name)
                with open('userdata.json','r') as json_file: 
                    userdata = json.load(json_file)
                for i in userdata['account']:
                    print('User: ' + i['username'] + '\t' + 'Password: ' + i['password'])
                print("-------------------------------------------")
                break
        else:
# If already existing user, check if the entered password is correct
            connection.send(str.encode('Username already existed, use another username'))
            print('Sign up failed')
    
    connection.close()

while True:
    Client, address = ServerSocket.accept()

    Client.send(b'1. Sign up\n2. Login\n3. Exit\n')
    choice = int(Client.recv(2048))
    
    if choice == 3:
        Client.close()
        break
    else:
        client_handler = threading.Thread(
            target=threaded_client,
            args=(Client,)  
        )
        client_handler.start()
        ThreadCount += 1
        print('Connection Request: ' + str(ThreadCount))
ServerSocket.close()
