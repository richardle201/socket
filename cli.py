import socket
from struct import *
import pickle
class SocketError(Exception):
    pass
class Socket:
    def __init__(self,host=socket.gethostname(),port=2345,verbose=0):
        self.host=host
        self.port=port
        self.SocketError=SocketError()
        self.verbose=verbose
        try:
            if self.verbose:
                print('SocketUtils:Creating Socket()')
            self.sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        except socket.error:
            raise SocketError('Error in Socket Object Creation!!')
    def Close(self):
        if self.verbose:
            print('SocketUtils:Closing socket!!')
        self.sock.close()
        if self.verbose:
            print('SocketUtils:Socket Closed!!')
class SocketClient(Socket):
    status = False
    def Connect(self,rhost=socket.gethostname(),rport=2345):
        self.rhost,self.rport=rhost,rport
        try:
            if self.verbose:
                print('Connecting to '+str(self.rhost)+' on port '+str(self.rport))
            self.sock.connect((self.rhost,self.rport))
            if self.verbose:
                self.status = True
                print('Connected !!!')
        except socket.error:
            raise SocketError('Connection refused to '+str(self.rhost)+' on port '+str(self.rport))
    def Send(self, obj):
        msg = pickle.dumps(obj)
        length = pack('>Q',len(msg))
        self.sock.sendall(length)
        self.sock.sendall(msg)
    def Receive(self):
        msg = bytearray()
        header = self.sock.recv(8)
        (length,) = unpack('>Q',header)
        length_recv = 0
        while length_recv < length:
            s = self.sock.recv(8192)
            msg += s
            length_recv += len(s)
        return pickle.loads(msg)
    # def Send(self,data):
    #     if self.verbose:
    #         print('Sending data of size ',len(data))
    #     if type(data) == str:
    #         data = data.encode()
    #     self.sock.sendall(data)
    #     if self.verbose:
    #         print('Data sent!!')
    # def Receive(self,size=1024):
    #     if self.verbose:
    #         print('Receiving data...')
    #     return self.sock.recv(size)
