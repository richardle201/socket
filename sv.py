import socket
import pyautogui
import os
import process
import keylog
import psutil
from struct import *
import pickle

def getListProcess():
    try:
        procs = []
        for proc in psutil.process_iter():
            with proc.oneshot():
                info = {}
                info['name'] = proc.name()
                info['id'] = proc.pid
                info['count_threads'] = proc.num_threads()
                procs.append(info)
        return procs
    except:
        return []
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
class SocketServer(Socket):
    def __init__(self,host=socket.gethostname(),port=2345,verbose=0):
        self.host,self.rhost=host,host
        self.port,self.rport=port,port
        self.verbose=verbose
        try:
            if self.verbose:
                print('SocketUtils:Creating SocketServer()')
            self.sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        except socket.error:
            raise SocketError('Failed to create SocketServer object!!')
        try:
            if self.verbose:
                print('SocketUtils:Binding Socket()')
            self.sock.bind((self.host,self.port))
            if self.verbose:
                print (self)
        except socket.error as msg:
            raise SocketError(msg)
    def Listen(self,msg='Accepted Connection from:'):
        if self.verbose:
            print('Listening to port')%self.port
        self.sock.listen(1)
        self.conn,self.rhost=self.sock.accept()
        self.rhost=self.rhost[0]
        if self.rhost:
            if self.verbose:
                print('Got connection from',self.rhost)
        print (msg,self.rhost)
    def Send(self, obj):
        msg = pickle.dumps(obj)
        length = pack('>Q',len(msg))
        self.conn.sendall(length)
        self.conn.sendall(msg)
    def Receive(self):
        msg = bytearray()
        header = self.conn.recv(8)
        (length,) = unpack('>Q',header)
        length_recv = 0
        while length_recv < length:
            s = self.conn.recv(8192)
            msg += s
            length_recv += len(s)
        return pickle.loads(msg)
    def Choices(self,msg):
        if msg == 'Connecting...':
            self.Send('Connected.')
        elif msg == 'Screenshot':
            img = pyautogui.screenshot()
            self.Send(img)
        elif msg == 'Shutdown':
            self.conn.close()
            self.Close()
            os.system("shutdown /s /t 1")
        elif msg == 'List process':
            listprocess = process.getListProcess()
            self.Send(listprocess)
        elif msg == 'Kill process':
            id = self.Receive()
            err=0
            listprocess = process.getListProcess()
            for value in listprocess:
                if str(value['id']) == id:
                    process.killProcess(id)
                    self.Send('???? di???t process')
                    err=err+1
                    break
            if err == 0:
                self.Send('Kh??ng t??m th???y process')
        elif msg == 'Start process':
            name = self.Receive()
            process.startProcess(name)
            self.Send('Process ???? ???????c b???t')
        elif msg =='List app':
            listapp = process.getListApp()
            self.Send(listapp)
        elif msg == 'Kill app':
            id = self.Receive()
            err=0
            listapp = process.getListApp()
            for app_id in listapp:
                if str(app_id['id']) == id:
                    process.killProcess(id)
                    self.Send('???? di???t ch????ng tr??nh')
                    err=1
            if err == 0:
                self.Send('Kh??ng t??m th???y ch????ng tr??nh')
        elif msg == 'Start app':
            name = self.Receive()
            process.startProcess(name)
            self.Send('Ch????ng tr??nh ???? ???????c b???t')
        elif msg =='Hook':
            keylog.start_keylog()
            hook_yet = True
            keylog.hook()
        elif msg == 'Unhook':
            keylog.unhook()
        elif msg == 'Print key':
            self.Send(keylog.get_key())
        elif msg == 'Quit':
            self.conn.close()
            self.Close()
            exit()


sv = SocketServer()
print(socket.gethostname())

while True:
    sv.Listen()
    while True:
        msg = sv.Receive()
        sv.Choices(msg)
    # sv.Send(msg)
    # msg = sv.Receive()
    # print('client n??i: ', msg)
    # if msg == 't???t m??? ??i':
        # break
sv.Close()
