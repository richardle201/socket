from tkinter import *
import tkinter.ttk as exTK
import socket
import os
import process
import keylog
import screen
from struct import *
import pickle
import socket_class as SC
class SocketServer(SC.Socket):
    def __init__(self,host=socket.gethostname(),port=2345):
        self.host,self.rhost=host,host
        self.port,self.rport=port,port
        try:
            self.sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        except socket.error:
            raise SC.SocketError('Failed to create SocketServer object!!')
        try:
            self.sock.bind((self.host,self.port))
        except socket.error as msg:
            raise SC.SocketError(msg)
    def Listen(self,msg='Accepted Connection from:'):
        self.sock.listen(1)
        self.conn,self.rhost=self.sock.accept()
        self.rhost=self.rhost[0]
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
        elif msg == 'Quit':
            self.conn.close()
            self.Close()
            exit()


def startServer():
    sv = SocketServer()
    while True:
        sv.Listen()
        while True:
            msg = sv.Receive()
            sv.Choices(msg)

win = Tk()
win.geometry('275x275')
win.title('Server')
exTK.Button(win,text='Mở server',command=startServer).place(relheight=0.6,
            relwidth=0.6,relx=0.2,rely=0.2)
win.mainloop()
