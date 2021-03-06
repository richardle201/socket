import socket
import threading
import os
import process
import keylog
import screen
import registry
from struct import *
import pickle
from tkinter import *
import tkinter.ttk as exTK
from tkinter import messagebox as mesTK
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
            if length - length_recv < 1024:
                s = self.conn.recv(length - length_recv)
            else:
                s = self.conn.recv(1024)
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
            os.system("shutdown /s /t 5")
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
        elif msg == 'import':
            data = self.Receive()
            if registry.import_filereg(data) == True:
                self.Send('Successful fix')
            else:
                self.Send('Fail fix')
        elif msg[0] == 'Get value':
            data = registry.getValue(msg[1],msg[2])
            self.Send(data)
        elif msg[0] == 'Set value':
            data = registry.setValue(msg[1],msg[2],msg[3],msg[4])
            self.Send(data)
        elif msg[0] == 'Delete value':
            data = registry.deleteValue(msg[1],msg[2])
            self.Send(data)
        elif msg[0] == 'Create key':
            data = registry.createKey(msg[1])
            self.Send(data)
        elif msg[0] == 'Delete key':
            data = registry.deleteKey(msg[1])
            self.Send(data)
        elif msg == 'Quit':
            self.conn.close()
            self.Close()
            exit()
        else:
            self.Send('L???i')

def notification(text):
    mesTK.showinfo(title='',message=text)

def startThread():
    while True:
        msg = sv.Receive()
        sv.Choices(msg)
def startServer():
    try:
        global sv
        sv = SocketServer()
        sv.Listen()
        thread = threading.Thread(target=startThread,daemon=TRUE)
        thread.start()
    except:
        notification('Server ???? ???????c m???')

win = Tk()
win.geometry('275x275+500+300')
win.title('Server')
exTK.Button(win,text='M??? server',command=startServer).place(relheight=0.6,
            relwidth=0.6,relx=0.2,rely=0.2)
win.mainloop()
