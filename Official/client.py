from tkinter import *
import tkinter.ttk as exTK
from tkinter import filedialog
from PIL import ImageTk, Image
from tkinter import scrolledtext as scrllT
from tkinter import messagebox as mesTK
import socket
from struct import *
import pickle
import socket_class as SC

class SocketClient(SC.Socket):
    def Connect(self, rhost=socket.gethostname(), rport=2345):
        self.rhost, self.rport = rhost, rport
        try:
            self.sock.connect((self.rhost, self.rport))
        except socket.error:
            raise SC.SocketError('Connection refused to ' +
                              str(self.rhost)+' on port '+str(self.rport))

    def Send(self, obj):
        msg = pickle.dumps(obj)
        length = pack('>Q', len(msg))
        self.sock.sendall(length)
        self.sock.sendall(msg)

    def Receive(self):
        msg = bytearray()
        header = self.sock.recv(8)
        (length,) = unpack('>Q', header)
        length_recv = 0
        while length_recv < length:
            if length - length_recv < 1024:
                s = self.sock.recv(length - length_recv)
            else:
                s = self.sock.recv(1024)
            msg += s
            length_recv += len(s)
        return pickle.loads(msg)


class monitor(Frame):
    def placeGUI(obj, e):
        if e.widget == obj:
            obj.update()
            objW = e.width
            objH = e.height
            obj.connect_.place(height=objH/14, width=objW /
                               4, x=objW*2/3, y=objH/14)
            obj.inputText.place(height=objH/14, width=objW /
                                7*4.15, x=objW/20, y=objH/14)
            obj.ProcessRunning_.place(
                height=objH*0.675, width=objW/10*2.2, x=objW/20, y=objH/10*1.775)
            obj.AppRunning_.place(
                height=objH*0.2, width=objW*0.355, x=objW*0.289, y=objH/10*1.775)
            obj.Shutdown_.place(height=objH*0.2, width=objW *
                                0.12, x=objW*0.289, y=objH*0.41)
            obj.ScreenCapture_.place(
                height=objH*0.2, width=objW*0.215, x=objW*0.43, y=objH*0.41)
            obj.Keystroke_.place(
                height=objH*0.43, width=objW*0.25, x=objW-objW/4-objW/12, y=objH/10*1.775)
            obj.EditRegistry_.place(
                height=objH*0.213, width=objW*0.49, x=objW*0.289, y=objH*0.64)
            obj.Exit_.place(height=objH*0.213, width=objW *
                            0.115, x=objW*0.8, y=objH*0.64)

    def __init__(obj, master):
        super().__init__(master)
        obj.inputText = exTK.Entry(obj, font='Calibri 12')
        obj.inputText.insert(END, 'Nhập IP')
        obj.connect_ = exTK.Button(obj, text='Kết nối', command=obj.connect)
        obj.ProcessRunning_ = exTK.Button(
            obj, text='Process\nRunning', command=process)
        obj.AppRunning_ = exTK.Button(obj, text='App Running', command=app)
        obj.Shutdown_ = exTK.Button(obj, text='Tắt\nmáy', command=Shutdown)
        obj.ScreenCapture_ = exTK.Button(
            obj, text='Chụp màn hình', command=ScreenShot)
        obj.Keystroke_ = exTK.Button(obj, text='Keystroke', command=keyStroke)
        obj.EditRegistry_ = exTK.Button(
            obj, text='Sửa Registry', command=fix_reg)
        obj.Exit_ = exTK.Button(obj, text='Thoát', command=quit_)
        master.bind('<Configure>', obj.placeGUI)

    def connect(obj):
        try:
            ip = str(obj.inputText.get())
            sock.Connect(rhost=ip)
            if checkConnect() == True:
                notification('Kết nối đến server thành công')
        except:
            notification('Lỗi kết nối đến server')

def checkConnect():
        try:
            sock.Send('Connecting...')
            if sock.Receive() == 'Connected.':
                return True
        except:
            return False

def notification(text):
    mesTK.showinfo(title='',message=text)

def guiStart():
    global windows
    windows = Tk()
    windows.title('Client')
    windows.geometry('700x600+100+100')
    GiaoDien = monitor(windows)
    GiaoDien.place(relwidth=1, relheight=1)
    windows.mainloop()


def quit_():
    global windows
    try:
        sock.Send('Quit')
        windows.destroy()
        return
    except:
        pass
    windows.destroy()


def ScreenShot():
    if checkConnect() == False:
        notification('Chưa kết nối đến server')
    else:
        class monitor2(Frame):
            def placeGUI(obj, e):
                if e.widget == obj:
                    obj.update()
                    objW = e.width
                    objH = e.height
                    obj.screen_.place(height=objH*0.575, width=objW *
                                      0.17, x=objW*0.785, y=objH/14)
                    obj.save_.place(height=objH*0.2, width=objW *
                                    0.17, x=objW*0.785, y=objH*0.75)
                    obj.panel.place(x=270, y=220, anchor="center")

            def __init__(obj, master):
                super().__init__(master)
                obj.panel = Label(obj)
                obj.screen_ = exTK.Button(
                    obj, text='Chụp', command=obj.TakePic)
                obj.save_ = exTK.Button(obj, text='Lưu', command=obj.saved)
                master.bind('<Configure>', obj.placeGUI)

            def saved(obj):
                global pic
                save_path = filedialog.asksaveasfilename(defaultextension='.png',
                                                         initialdir='/', title='Save As', filetypes=(('All file', '*.*'), ('png file', '*.png')))
                if not save_path:
                    return
                pic.save(save_path)

            def TakePic(obj):
                global img, pic
                sock.Send('Screenshot')
                pic = sock.Receive()
                width, height = pic.size
                img = pic.resize(
                    (int(width / 4), int(height / 4)), Image.ANTIALIAS)
                img = ImageTk.PhotoImage(img)
                obj.panel.configure(image=img)
                return

        def guiScreen():
            win = Toplevel()
            win.title('Pic')
            win.geometry('700x500+125+125')
            GiaoDien = monitor2(win)
            GiaoDien.place(relwidth=1, relheight=1)
            win.grab_set()
        guiScreen()


def process():
    def xem():
        try:
            xoa()
            sock.Send('List process')
            procs = sock.Receive()
            i = 0
            for value in procs:
                tmp = str(value['name'])
                tmp = tmp.split('.exe')
                output.insert(parent='', index=i, iid=i, values=(
                    tmp[0], value['id'], value['count_threads']))
                i = i+1
        except:
            return

    def kill():
        root = Toplevel()
        root.title('Kill')
        root.geometry('450x100+150+150')
        inputText = exTK.Entry(root, font='Car 12')
        inputText.place(relheight=0.35, relwidth=0.6, relx=0.05, rely=0.25)
        inputText.insert(END, 'Nhập ID')
        try:
            def action():
                sock.Send('Kill process')
                id = inputText.get()
                sock.Send(id)
                note = sock.Receive()
                notification(note)
            action_ = exTK.Button(root, text='Kill', command=action).place(
                relheight=0.35, relwidth=0.25, relx=0.7, rely=0.25)
        except:
            return
        root.grab_set()

    def start():
        root = Toplevel()
        root.title('Start')
        root.geometry('450x100+150+150')
        inputText = exTK.Entry(root, font='Calibri 12')
        inputText.insert(END, 'Nhập tên')
        inputText.place(relheight=0.35, relwidth=0.6, relx=0.05, rely=0.25)
        try:
            def action():
                sock.Send('Start process')
                name = inputText.get()
                sock.Send(name)
                note = sock.Receive()
                notification(note)
            action_ = exTK.Button(root, text='Start', command=action).place(
                relheight=0.35, relwidth=0.25, relx=0.7, rely=0.25)
        except:
            return
        root.grab_set()

    def xoa():
        global output
        for i in output.get_children():
            output.delete(i)
        win.update()

    if checkConnect() == False:
        notification('Chưa kết nối đến server')
    else:
        win = Toplevel()
        win.title('Process')
        win.geometry('500x500+200+220')
        kill_ = exTK.Button(win, text='Kill', command=kill).place(
            relheight=0.1, relwidth=0.2, relx=0.075, rely=0.075)
        xem_ = exTK.Button(win, text='Xem', command=xem).place(
            relheight=0.1, relwidth=0.2, relx=0.3, rely=0.075)
        xoa_ = exTK.Button(win, text='Xoá', command=xoa).place(
            relheight=0.1, relwidth=0.2, relx=0.525, rely=0.075)
        start_ = exTK.Button(win, text='Start', command=start).place(
            relheight=0.1, relwidth=0.2, relx=0.75, rely=0.075)
        global output
        output = exTK.Treeview(win)

        sb = Scrollbar(win, orient=VERTICAL)
        sb.place(relheight=0.7, relwidth=0.05, relx=0.9, rely=0.225)
        output.config(yscrollcommand=sb.set)
        sb.config(command=output.yview)

        output['columns'] = ('1', '2', '3')
        output.column('#0', width=0, stretch=NO)
        output.column('1', anchor=W, width=10)
        output.column('2', anchor=W, width=10)
        output.column('3', anchor=W, width=10)

        output.heading('#0', text='', anchor=CENTER)
        output.heading('1', text='Name process', anchor=CENTER)
        output.heading('2', text='ID Process', anchor=CENTER)
        output.heading('3', text='Count Thread', anchor=CENTER)
        output.place(relheight=0.7, relwidth=0.825, relx=0.075, rely=0.225)

        win.grab_set()


def app():
    if checkConnect() == False:
        notification('Chưa kết nối đến server')
    else:
        def xem():
            try:
                xoa()
                sock.Send('List app')
                data = sock.Receive()
                i = 0
                for value in data:
                    tmp = str(value['name'])
                    tmp = tmp.split('.exe')
                    output.insert(parent='', index=i, iid=i, values=(
                        tmp[0], value['id'], value['count_threads']))
                    i = i+1
            except:
                return

        def kill():
            root = Toplevel()
            root.title('Kill')
            root.geometry('450x100+125+125')
            inputText = exTK.Entry(root, font='Car 12')
            inputText.place(relheight=0.35, relwidth=0.6, relx=0.05, rely=0.25)
            inputText.insert(END, 'Nhập ID')
            try:
                def action():
                    sock.Send('Kill app')
                    id = inputText.get()
                    sock.Send(id)
                    note = sock.Receive()
                    notification(note)
                action_ = exTK.Button(root, text='Kill', command=action).place(
                    relheight=0.35, relwidth=0.25, relx=0.7, rely=0.25)
            except:
                return
            root.grab_set()

        def start():
            root = Toplevel()
            root.title('Start')
            root.geometry('450x100+150+150')
            inputText = exTK.Entry(root, font='Calibri 12')
            inputText.insert(END, 'Nhập tên')
            inputText.place(relheight=0.35, relwidth=0.6, relx=0.05, rely=0.25)
            try:
                def action():
                    sock.Send('Start app')
                    name = inputText.get()
                    sock.Send(name)
                    note = sock.Receive()
                    notification(note)
                action_ = exTK.Button(root, text='Start', command=action).place(
                    relheight=0.35, relwidth=0.25, relx=0.7, rely=0.25)
            except:
                return
            root.grab_set()

        def xoa():
            global output
            for i in output.get_children():
                output.delete(i)
            win.update()

        win = Toplevel()
        win.title('listApp')
        win.geometry('500x500+200+220')
        kill_ = exTK.Button(win, text='Kill', command=kill).place(
            relheight=0.1, relwidth=0.2, relx=0.075, rely=0.075)
        xem_ = exTK.Button(win, text='Xem', command=xem).place(
            relheight=0.1, relwidth=0.2, relx=0.3, rely=0.075)
        xoa_ = exTK.Button(win, text='Xoá', command=xoa).place(
            relheight=0.1, relwidth=0.2, relx=0.525, rely=0.075)
        start_ = exTK.Button(win, text='Start', command=start).place(
            relheight=0.1, relwidth=0.2, relx=0.75, rely=0.075)
        global output
        output = exTK.Treeview(win)

        sb = Scrollbar(win, orient=VERTICAL)
        sb.place(relheight=0.7, relwidth=0.05, relx=0.9, rely=0.225)
        output.config(yscrollcommand=sb.set)
        sb.config(command=output.yview)

        output['columns'] = ('1', '2', '3')
        output.column('#0', width=0, stretch=NO)
        output.column('1', anchor=W, width=10)
        output.column('2', anchor=W, width=10)
        output.column('3', anchor=W, width=10)

        output.heading('#0', text='', anchor=CENTER)
        output.heading('1', text='Name Application', anchor=CENTER)
        output.heading('2', text='ID Application', anchor=CENTER)
        output.heading('3', text='Count Thread', anchor=CENTER)
        output.place(relheight=0.7, relwidth=0.825, relx=0.075, rely=0.225)

        win.grab_set()


def keyStroke():
    if checkConnect() == False:
        notification('Chưa kết nối đến server')
    else:
        win = Toplevel()
        win.title('Keystroke')
        win.geometry('500x500+200+220')

        def hook():
                sock.Send('Hook')

        def unhook():
                sock.Send('Unhook')

        def xoa():
            global output_key
            output_key.configure(state=NORMAL)
            output_key.delete('1.0', END)

        def inphim():
            try:
                sock.Send('Print key')
                global output_key
                data = sock.Receive()
                output_key.configure(state=NORMAL)
                while True:
                    if data.find('enter') == -1:
                        output_key.insert(END, data)
                        break
                    else:
                        tmp = data.split('enter', 1)
                        output_key.insert(END, tmp[0])
                        output_key.insert(END, 'enter\n')
                        data = tmp[1]
                output_key.configure(state=DISABLED)
            except:
                return

        hook_ = exTK.Button(win, text='Hook', command=hook).place(
            relheight=0.1, relwidth=0.2, relx=0.04, rely=0.075)
        unhook_ = exTK.Button(win, text='Unhook', command=unhook).place(
            relheight=0.1, relwidth=0.2, relx=0.28, rely=0.075)
        inphim_ = exTK.Button(win, text='In phím', command=inphim).place(
            relheight=0.1, relwidth=0.2, relx=0.52, rely=0.075)
        xoa_ = exTK.Button(win, text='Xoá', command=xoa).place(
            relheight=0.1, relwidth=0.2, relx=0.76, rely=0.075)

        global output_key
        output_key = scrllT.ScrolledText(
            win, font='Calibri 12', state=DISABLED)
        output_key.place(relheight=0.6, relwidth=0.88, relx=0.04, rely=0.25)

        win.grab_set()


def fix_reg():
    if checkConnect() == False:
        notification('Chưa kết nối đến server')
    else:
        win = Toplevel()
        win.title('registry')
        win.geometry('500x500+200+225')

        def browser():
            global path_, content_
            link = filedialog.askopenfilename(filetypes=(
                ("reg file", "*.Reg"), ("All files", "*.*")))
            if not link:
                return
            path_.configure(state=NORMAL)
            path_.delete('1.0', END)
            path_.insert(END, link)
            path_.configure(state=DISABLED)
            content_.delete('1.0', END)
            link = open(link)
            data = link.read()
            content_.insert(END, data)
            link.close()

        def sendContent():
            try:
                global content_
                data = content_.get('1.0', END)
                if data =='':
                    notification('Chưa nhập nội dung')
                    return
                sock.Send('import')
                sock.Send(data)
                note = sock.Receive()
                if note == 'Successful fix':
                    notification('Sửa thành công')
                elif note == 'Fail fix':
                    notification('Sửa thất bại')
            except:
                notification('Lỗi')

        def function_(temp):
            global func_, nameValue_, value_, typedata_
            fun = func_.get()
            if fun == 'Get value':
                nameValue_.place(relheight=0.05, relwidth=0.27,
                                 relx=0.06, rely=0.575)
                value_.place_forget()
                typedata_.place_forget()
            if fun == 'Set value':
                nameValue_.place(relheight=0.05, relwidth=0.27,
                                 relx=0.06, rely=0.575)
                value_.place(relheight=0.05, relwidth=0.27,
                             relx=0.35, rely=0.575)
                typedata_.place(relheight=0.05, relwidth=0.27,
                                relx=0.64, rely=0.575)
            if fun == 'Delete value':
                nameValue_.place(relheight=0.05, relwidth=0.27,
                                 relx=0.06, rely=0.575)
                value_.place_forget()
                typedata_.place_forget()
            if fun == 'Create key':
                nameValue_.place_forget()
                value_.place_forget()
                typedata_.place_forget()
            if fun == 'Delete key':
                nameValue_.place_forget()
                value_.place_forget()
                typedata_.place_forget()

        def send():
            global func_, path2_, nameValue_, value_, typedata_, content2_
            try:
                data = [func_.get(),path2_.get('1.0', END),nameValue_.get('1.0', END),value_.get('1.0', END),typedata_.get()]
                sock.Send(data)
                message = sock.Receive()
                content2_.configure(state=NORMAL)
                content2_.insert(END, message + '\n')
                content2_.configure(state=DISABLED)
            except:
                notification('Lỗi')

        def Delete():
            global content2_
            content2_.configure(state=NORMAL)
            content2_.delete('1.0', END)
            content2_.configure(state=DISABLED)

        global path_, content_, func_, path2_, nameValue_, value_, typedata_, content2_
        path_ = Text(win, font=('Calibri', 12))
        path_.place(relheight=0.05, relwidth=0.7, relx=0.04, rely=0.05)
        path_.insert(END, 'Đường dẫn...')
        path_.configure(state=DISABLED)
        browse_ = exTK.Button(win, text='Browser...', command=browser).place(
            relheight=0.05, relwidth=0.2, relx=0.77, rely=0.05)

        content_ = scrllT.ScrolledText(win, font=('Calibri', 12))
        content_.place(relheight=0.2, relwidth=0.7, relx=0.04, rely=0.125)
        content_.insert(END, 'Nội dung')

        sendContent_ = exTK.Button(win, text='Gửi nội dung', command=sendContent).place(
            relheight=0.2, relwidth=0.2, relx=0.77, rely=0.125)

        label = LabelFrame(win, text='Sửa giá trị trực tiếp')
        label.place(relheight=0.575, relwidth=0.9, relx=0.04, rely=0.35)

        func_ = exTK.Combobox(win, width=30, font='Calibri 12')
        func_.place(relheight=0.05, relwidth=0.85, relx=0.06, rely=0.425)
        func_['values'] = ('Get value', 'Set value',
                           'Delete value', 'Create key', 'Delete key')
        func_.insert(END, 'Chọn chức năng')
        func_.bind('<<ComboboxSelected>>', function_)

        path2_ = Text(win, font=('Calibri', 12))
        path2_.place(relheight=0.05, relwidth=0.85, relx=0.06, rely=0.5)
        path2_.insert(END, 'Đường dẫn')

        nameValue_ = Text(win, font=('Calibri', 12))
        nameValue_.place(relheight=0.05, relwidth=0.27, relx=0.06, rely=0.575)
        nameValue_.insert(END, 'Name value')

        value_ = Text(win, font=('Calibri', 12))
        value_.place(relheight=0.05, relwidth=0.27, relx=0.35, rely=0.575)
        value_.insert(END, 'Value')

        typedata_ = exTK.Combobox(win, width=30, font='Calibri 12')
        typedata_.place(relheight=0.05, relwidth=0.27, relx=0.64, rely=0.575)
        typedata_['values'] = ('String', 'Binary', 'DWORD',
                               'QWORD', 'Multi-String', 'Expandable String')
        typedata_.insert(END, 'Kiểu dữ liệu')

        content2_ = scrllT.ScrolledText(win, font=('Calibri', 12))
        content2_.place(relheight=0.175, relwidth=0.85, relx=0.06, rely=0.65)

        send_ = exTK.Button(win, text='Gửi',command=send).place(
            relheight=0.05, relwidth=0.2, relx=0.25, rely=0.85)

        delete_ = exTK.Button(win, text='Xoá', command=Delete).place(
            relheight=0.05, relwidth=0.2, relx=0.55, rely=0.85)
        win.grab_set()


def Shutdown():
    if checkConnect() == False:
        notification('Chưa kết nối đến server')
    else:
        sock.Send('Shutdown')


def start_client():
    global sock
    sock = SocketClient()


start_client()
guiStart()
