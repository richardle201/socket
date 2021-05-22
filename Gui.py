from tkinter import *
import tkinter.ttk as exTK
from tkinter import filedialog
import pyautogui
import pickle
from PIL import ImageTk, Image
import os
import signal
import psutil


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
        obj.Shutdown_ = exTK.Button(obj, text='Tắt\nmáy')
        obj.ScreenCapture_ = exTK.Button(
            obj, text='Chụp màn hình', command=ScreenShot)
        obj.Keystroke_ = exTK.Button(obj, text='Keystroke')
        obj.EditRegistry_ = exTK.Button(obj, text='Sửa Registry')
        obj.Exit_ = exTK.Button(obj, text='Thoát', command=quit)
        master.bind('<Configure>', obj.placeGUI)
    def connect(obj):
        ip = str(obj.inputText.get())



def guiStart():
    global win
    win = Tk()
    win.title('Client')
    win.geometry('700x600')
    GiaoDien = monitor(win)
    GiaoDien.place(relwidth=1, relheight=1)
    win.mainloop()
    
def quit():
    global win
    try:
        #gửi thông tin cho server ở đây
        win.destroy()
        return
    except:
        pass
    win.destroy()


def ScreenShot():
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
            im = pyautogui.screenshot()
            data = pickle.dumps(im)
            pic = pickle.loads(data)
            width, height = pic.size
            img = pic.resize((int(width / 4), int(height / 4)), Image.ANTIALIAS)
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

    def startProcess(process_name):
        os.system('start ' + process_name)


    def killProcess(pid):
        os.kill(int(pid), signal.SIGTERM)


    def xem():
        data = getListProcess()
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
        inputText.insert(END,'Nhập ID')

        def action():
            ID = inputText.get()
        action_ = exTK.Button(root, text='Kill', command=action).place(
            relheight=0.35, relwidth=0.25, relx=0.7, rely=0.25)
        root.mainloop()

    def start():
        root = Toplevel()
        root.title('Start')
        root.geometry('450x100')
        inputText = exTK.Entry(root ,font='Calibri 12')
        inputText.insert(END,'Nhập tên')
        inputText.place(relheight=0.35, relwidth=0.6, relx=0.05, rely=0.25)
        
        def action():
            ID=inputText.get()
        action_ = exTK.Button(root, text='Start', command=action).place(
            relheight=0.35, relwidth=0.25, relx=0.7, rely=0.25)
        root.mainloop()

    def xoa():
        global output
        for i in output.get_children():
            output.delete(i)
        win.update()

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

guiStart()
