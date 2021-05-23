from tkinter import *
import tkinter.ttk as exTK
from tkinter import filedialog
import pyautogui
import pickle
from PIL import ImageTk, Image
import os
import signal
import psutil
import subprocess
from tkinter import scrolledtext as scrllT
import cli

global status
status = False

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
        obj.inputText.insert(END,'Nhập IP')
        obj.connect_ = exTK.Button(obj, text='Kết nối', command=obj.connect)
        obj.ProcessRunning_ = exTK.Button(
            obj, text='Process\nRunning', command=process)
        obj.AppRunning_ = exTK.Button(obj, text='App Running', command=app)
        obj.Shutdown_ = exTK.Button(obj, text='Tắt\nmáy', command=Shutdown)
        obj.ScreenCapture_ = exTK.Button(
            obj, text='Chụp màn hình', command=ScreenShot)
        obj.Keystroke_ = exTK.Button(obj, text='Keystroke', command=keyStroke)
        obj.EditRegistry_ = exTK.Button(obj, text='Sửa Registry', command=fix_reg)
        obj.Exit_ = exTK.Button(obj, text='Thoát', command=quit)
        master.bind('<Configure>', obj.placeGUI)

    def connect(obj):
        try:
            ip = str(obj.inputText.get())
            sock.Connect(rhost=ip)
            sock.Send('Connecting...')
            if sock.Receive().decode() == 'Connected.':
                sock.status=True
            connect_notification()
        except:
            connect_notification()


def connect_notification():
    def OK():
        root.destroy()
    if sock.status==False:
        text_ = 'Lỗi kết nối đến server'
        sock.status=True
    else:
        text_='Kết nối đến server thành công'
    root = Toplevel()
    root.title('')
    root.geometry('300x200')
    label = Label(root,text=text_)
    label.place(relheight=0.5, relwidth=0.7,relx=0.1,rely=0.1)
    OK_ = exTK.Button(root,text='OK',command=OK)
    OK_.place(relheight=0.2, relwidth=0.45,relx=0.45,rely=0.7)
    root.mainloop()

def guiStart():
    global windows
    windows = Tk()
    windows.title('Client')
    windows.geometry('700x600')
    GiaoDien = monitor(windows)
    GiaoDien.place(relwidth=1, relheight=1)
    windows.mainloop()

def quit():
    global windows
    try:
        sock.Send('Quit')
        windows.destroy()
        return
    except:
        pass
    windows.destroy()

def notConnect():
    def OK():
        root.destroy()
    root = Toplevel()
    root.title('')
    root.geometry('250x200')
    label = Label(root,text='Chưa kết nối đến server')
    label.place(relheight=0.5, relwidth=0.7,relx=0.1,rely=0.1)
    OK_ = exTK.Button(root,text='OK',command=OK)
    OK_.place(relheight=0.2, relwidth=0.45,relx=0.45,rely=0.7)
    root.mainloop()

def ScreenShot():
    if sock.status == False:
        notConnect()
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
                obj.screen_ = exTK.Button(obj, text='Chụp', command=obj.TakePic)
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
                data = b""
                while True:
                    packet = sock.Receive()
                    if not packet: break
                    data += packet
                pic = pickle.loads(data)
               # data = sock.Receive()
               # pic = pickle.loads(data)
                width, height = pic.size
                img = pic.resize(
                    (int(width / 4), int(height / 4)), Image.ANTIALIAS)
                img = ImageTk.PhotoImage(img)
                obj.panel.configure(image=img)
                return

        def guiScreen():
            win = Toplevel()
            win.title('Pic')
            win.geometry('700x600')
            GiaoDien = monitor2(win)
            GiaoDien.place(relwidth=1, relheight=1)
            win.mainloop()
        guiScreen()


def process():
    #3 hàm bên dưới là của server
    # def getListProcess():
    #     try:
    #         procs = []
    #         for proc in psutil.process_iter():
    #             with proc.oneshot():
    #                 info = {}
    #                 info['name'] = proc.name()
    #                 info['id'] = proc.pid
    #                 info['count_threads'] = proc.num_threads()
    #                 procs.append(info)
    #         return procs
    #     except:
    #         return []

    # def startProcess(process_name):
    #     os.system('start ' + process_name)

    # def killProcess(pid):
    #     os.kill(int(pid), signal.SIGTERM)
    #client
    def xem():
        #Thay data = nhận dữ liệu từ server
        sock.Send('List process')
        data = sock.Receive()
        procs = pickle.loads(data)
        i = 0
        for value in procs:
            tmp = str(value['name'])
            tmp = tmp.split('.exe')
            output.insert(parent='', index=i, iid=i, values=(
                tmp[0], value['id'], value['count_threads']))
            i = i+1

    def kill():
        root = Toplevel()
        root.title('Kill')
        root.geometry('450x100')
        inputText = exTK.Entry(root, font='Car 12')
        inputText.place(relheight=0.35, relwidth=0.6, relx=0.05, rely=0.25)
        inputText.insert(END, 'Nhập ID')
        sock.Send('Kill process')
        def action():
            id = inputText.get()
            sock.Send(id)
            #Gửi ID qua cho server
            # killProcess(ID) dòng này test chức năng
        action_ = exTK.Button(root, text='Kill', command=action).place(
            relheight=0.35, relwidth=0.25, relx=0.7, rely=0.25)
        root.mainloop()
    def start():
            root = Toplevel()
            root.title('Start')
            root.geometry('450x100')
            inputText = exTK.Entry(root, font='Calibri 12')
            inputText.insert(END, 'Nhập tên')
            inputText.place(relheight=0.35, relwidth=0.6, relx=0.05, rely=0.25)
            sock.Send('Start process')
            def action():
                name = inputText.get()
                sock.Send(name)
                #Gửi name qua cho server
                #startProcess(name) dòng này test chức năng
            action_ = exTK.Button(root, text='Start', command=action).place(
                relheight=0.35, relwidth=0.25, relx=0.7, rely=0.25)
            root.mainloop()

    def xoa():
        global output
        for i in output.get_children():
            output.delete(i)
        win.update()

    if sock.status == False:
        notConnect()
    else:
        

        win = Toplevel()
        win.title('Process')
        win.geometry('500x500')
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

        win.mainloop()

def app():

    # 3 hàm dưới của server
    def getListApp():
        try:
            cmd = 'powershell "gps | where {$_.MainWindowTitle } | select Id'
            proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
            pids = []
            for line in proc.stdout:
                try:
                    pids.append(int(line.decode().rstrip()))
                except ValueError:
                    pass
            apps = []
            for pid in pids:
                try:
                    proc = psutil.Process(pid)
                    with proc.oneshot():
                        info = {}
                        info['name'] = proc.name()
                        info['id'] = proc.pid
                        info['count_threads'] = proc.num_threads()
                        apps.append(info)
                except psutil.NoSuchProcess:
                    pass
            return apps
        except:
            return []


    def startProcess(process_name):
        os.system('start ' + process_name)


    def killProcess(pid):
        os.kill(int(pid), signal.SIGTERM)

    # client
    if sock.status == False:
        notConnect()
    else:
        def xem():
            sock.Send('List app')
            #Sửa data nhận dữ liệu từ server
            data = sock.Receive().decode()
            i = 0
            for value in data:
                tmp = str(value['name'])
                tmp = tmp.split('.exe')
                output.insert(parent='', index=i, iid=i, values=(
                    tmp[0], value['id'], value['count_threads']))
                i = i+1


        def kill():
            root = Toplevel()
            root.title('Kill')
            root.geometry('450x100')
            inputText = exTK.Entry(root, font='Car 12')
            inputText.place(relheight=0.35, relwidth=0.6, relx=0.05, rely=0.25)
            inputText.insert(END, 'Nhập ID')
            sock.Send('Kill app')
            def action():
                id = inputText.get()
                sock.Send(id)
                #Gửi ID cho server
                #killProcess(ID)
            action_ = exTK.Button(root, text='Kill', command=action).place(
                relheight=0.35, relwidth=0.25, relx=0.7, rely=0.25)
            root.mainloop()


        def start():
            root = Toplevel()
            root.title('Start')
            root.geometry('450x100')
            inputText = exTK.Entry(root, font='Calibri 12')
            inputText.insert(END, 'Nhập tên')
            inputText.place(relheight=0.35, relwidth=0.6, relx=0.05, rely=0.25)
            sock.Send('Start app')
            def action():
                name = inputText.get()
                sock.Send(name)
                #Gửi name cho server
                #startProcess(name)
            action_ = exTK.Button(root, text='Start', command=action).place(
                relheight=0.35, relwidth=0.25, relx=0.7, rely=0.25)
            root.mainloop()


        def xoa():
            global output
            for i in output.get_children():
                output.delete(i)
            win.update()


        win = Toplevel()
        win.title('listApp')
        win.geometry('500x500')
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

        win.mainloop()

def keyStroke():
    if sock.status == False:
        notConnect()
    else:
        win = Toplevel()
        win.title('Keystroke')
        win.geometry('500x500')
        sock.Send('Keystroke')
        def hook():
            sock.Send('Hook')
            #Gửi báo hiệu keylog
            a='' #Để cho đỡ báo lỗi

        def unhook():
            sock.Send('Unhook')
            #Gửi báo hiệu thoát keylog
            a=''

        def xoa():
            global output_key
            output_key.configure(state=NORMAL)
            output_key.delete('1.0', END)


        def inphim():
            global output_key
            data = sock.Receive().decode()   #Dữ liệu nhận từ server 
            output_key.configure(state=NORMAL)
            output_key.insert(END,data)
            output_key.configure(state=DISABLED)

        hook_ = exTK.Button(win, text='Hook').place(
            relheight=0.1, relwidth=0.2, relx=0.04, rely=0.075)
        unhook_ = exTK.Button(win, text='Unhook').place(
            relheight=0.1, relwidth=0.2, relx=0.28, rely=0.075)
        inphim_ = exTK.Button(win, text='In phím',command=inphim).place(
            relheight=0.1, relwidth=0.2, relx=0.52, rely=0.075)
        xoa_ = exTK.Button(win, text='Xoá',command=xoa).place(
            relheight=0.1, relwidth=0.2, relx=0.76, rely=0.075)

        global output_key
        output_key = scrllT.ScrolledText(win, font='Calibri 12',state=DISABLED)
        output_key.place(relheight=0.6, relwidth=0.88, relx=0.04, rely=0.25)

        win.mainloop()

def fix_reg():
    if sock.status == False:
        notConnect()
    else:
        win = Toplevel()
        win.title('registry')
        win.geometry('500x500')

        def browser():
            global path_, content_
            link = filedialog.askopenfilename(filetypes=(
                ("reg file", "*.Reg"), ("All files", "*.*")))
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
            global content_
            data = content_.get('1.0', END)
            #Gửi dữ liệu qua server

        global path_, content_,func,path2_,nameValue
        path_ = Text(win, font=('Calibri', 12))
        path_.place(relheight=0.05, relwidth=0.7, relx=0.04, rely=0.05)
        path_.insert(END,'Đường dẫn...')
        path_.configure(state=DISABLED)
        browse_ = exTK.Button(win, text='Browser...', command=browser).place(
            relheight=0.05, relwidth=0.2, relx=0.77, rely=0.05)

        content_ = scrllT.ScrolledText(win, font=('Calibri', 12))
        content_.place(relheight=0.2, relwidth=0.7, relx=0.04, rely=0.125)
        content_.insert(END,'Nội dung')

        sendContent_ = exTK.Button(win, text='Gửi nội dung', command=sendContent).place(
            relheight=0.2, relwidth=0.2, relx=0.77, rely=0.125)

        label = LabelFrame(win,text='Sửa giá trị trực tiếp')
        label.place(relheight=0.575, relwidth=0.9, relx=0.04, rely=0.35)

        func_ = exTK.Combobox(win, width=30, font='Calibri 12')
        func_.place(relheight=0.05, relwidth=0.85, relx=0.06, rely=0.425)
        func_['values']=('Get value','Set value','Delete value','Create key','Delete key')
        func_.insert(END,'Chọn chức năng')

        path2_ = Text(win, font=('Calibri', 12))
        path2_.place(relheight=0.05, relwidth=0.85, relx=0.06, rely=0.5)
        path2_.insert(END,'Đường dẫn')

        nameValue_ = Text(win, font=('Calibri', 12))
        nameValue_.place(relheight=0.05, relwidth=0.27, relx=0.06, rely=0.575)
        nameValue_.insert(END,'Name value')

        Value_ = Text(win, font=('Calibri', 12))
        Value_.place(relheight=0.05, relwidth=0.27, relx=0.35, rely=0.575)
        Value_.insert(END,'Value')

        typedata_ = exTK.Combobox(win, width=30, font='Calibri 12')
        typedata_.place(relheight=0.05, relwidth=0.27, relx=0.64, rely=0.575)
        typedata_['values']=('String','Binary','DWORD','QWORD','Multi-String','Expandable String')
        typedata_.insert(END,'Kiểu dữ liệu')

        content2_ = scrllT.ScrolledText(win, font=('Calibri', 12))
        content2_.place(relheight=0.175, relwidth=0.85, relx=0.06, rely=0.65)

        send_ = exTK.Button(win, text='Gửi').place(
            relheight=0.05, relwidth=0.2, relx=0.25, rely=0.85)

        delete_ = exTK.Button(win, text='Xoá').place(
            relheight=0.05, relwidth=0.2, relx=0.55, rely=0.85)
        win.mainloop()

def Shutdown():
    if sock.status == False:
        notConnect()
    else:
        sock.Send('Shutdown')
def start_client():
    global sock
    sock = cli.SocketClient()
start_client()
guiStart()
