import socket

def TAKEPIC():
    screenshot_data = s.recv(2048)
    # print(screenshot_data)
    with open('new_screenshot.png','wb') as f:
        f.write(screenshot_data)
# Create a socket object 
# s = socket.socket()         
ip = socket.gethostname()
# Define the port on which you want to connect 
port = 12345    
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((ip, port)) 
while True:
    choice = input('Enter choice: ')
    s.send(choice.encode())
    # if s == 'TAKEPIC':
    #     takepic()
    # # receive data from the server 
    # # close the connection 
    # elif s == 'QUIT': break
    if choice == 'KEYLOG':
        #keylog.start_keylog()
        break
    elif choice == 'SHUTDOWN':
        break
    # # elif choice =='REGISTRY':
    # #     registry()
    # #     break
    elif choice == 'TAKEPIC':
        TAKEPIC()
        break
    # # elif choice == 'PROCESS':
    # #     process()
    # #     break
    # # elif choice == 'APPLICATION':
    # #     application()
    # #     break
    elif choice == 'QUIT': break
s.close()

