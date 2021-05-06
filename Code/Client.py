import socket


# create an ipv4 (AF_INET) socket object using the tcp protocol (SOCK_STREAM)
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostname()
port = 1233
# connect the client
# client.connect((target, port))
client.connect((host, port))

while True:

	response = client.recv(2048)
	# Input UserName
	name = input(response.decode())	
	client.send(str.encode(name))
	response = client.recv(2048)
	# Input Password
	password = input(response.decode())	
	client.send(str.encode(password))

	''' Response : Status of Connection :
		1 : Registeration successful 
		2 : Username already existed
	'''
	# Receive response 
	response = client.recv(2048)
	response = response.decode()

	print(response)
	if response == 'Registeration Successful':
		client.close()
		break
