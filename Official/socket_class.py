import socket
class SocketError(Exception):
    pass
class Socket:
    def __init__(self,host=socket.gethostname(),port=2345):
        self.host=host
        self.port=port
        self.SocketError=SocketError()
        try:
            self.sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        except socket.error:
            raise SocketError('Error in Socket Object Creation!!')
    def Close(self):
        self.sock.close()
