import socket


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)        
print ("Socket successfully created")
ip = socket.gethostname()
print(ip)

port = 2345                
  
s.bind((ip, port))         
print ("socket binded to %s" %(port)) 
  
s.listen(100)     
print ("socket is listening")            

while True: 
  
# Establish connection with client. 
    conn, addr = s.accept()     
    print ('Got connection from', addr )
    conn.send(b'Connecting...')
    conn.close()
# Close the connection with the client 
s.close()
