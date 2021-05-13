from tkinter import *
import tkinter.ttk as exTK


class monitor(Frame):
    def placeGUI(obj, e):
        obj.update()
        objW = obj.winfo_width()
        objH = obj.winfo_height()
        obj.connect_.place(height=objH/14, width=objW/4, x=objW-objW/4-objW/12, y=objH/14)
        obj.inputText.place(height=objH/14, width=objW/7*4.15, x=objW/20, y=objH/14)
        obj.ProcessRunning_.place(height=objH*0.675, width=objW/10*2.2, x=objW/20, y=objH/10*1.775)
        obj.AppRunning_.place(height=objH*0.2, width=objW*0.355, x=objW*0.289, y=objH/10*1.775)
        obj.Shutdown_.place(height=objH*0.2, width=objW*0.12, x=objW*0.289, y=objH*0.41)
        obj.ScreenCapture_.place(height=objH*0.2, width=objW*0.215, x=objW*0.43, y=objH*0.41)
        obj.Keystroke_.place(height=objH*0.43, width=objW*0.25, x=objW-objW/4-objW/12, y=objH/10*1.775)
        obj.EditRegistry_.place(height=objH*0.213, width=objW*0.49, x=objW*0.289, y=objH*0.64)
        obj.Exit_.place(height=objH*0.213, width=objW*0.115, x=objW*0.8, y=objH*0.64)
    def __init__(obj, master):
        super().__init__(master)
        obj.inputText = exTK.Entry(obj)
        obj.connect_ = exTK.Button(obj, text='Kết nối')
        obj.ProcessRunning_ = exTK.Button(obj, text='Process Running')
        obj.AppRunning_ = exTK.Button(obj, text='App Running')
        obj.Shutdown_ = exTK.Button(obj, text='Tắt máy')
        obj.ScreenCapture_ = exTK.Button(obj, text='Chụp màn hình')
        obj.Keystroke_ = exTK.Button(obj, text='Keystroke')
        obj.EditRegistry_ = exTK.Button(obj, text='Sửa Registry')
        obj.Exit_ = exTK.Button(obj, text='Thoát')
        master.bind('<Configure>', obj.placeGUI)


win = Tk()
win.title('Client')
win.geometry('450x400')
GiaoDien = monitor(win)
GiaoDien.place(relwidth=1, relheight=1)
win.mainloop()
