from tkinter import *
import tkinter.ttk as exTK
from tkinter import filedialog
import pyautogui
import pickle
from PIL import ImageTk, Image


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
        obj.inputText = exTK.Entry(obj)
        obj.connect_ = exTK.Button(obj, text='Kết nối', command=obj.connect)
        obj.ProcessRunning_ = exTK.Button(obj, text='Process Running')
        obj.AppRunning_ = exTK.Button(obj, text='App Running')
        obj.Shutdown_ = exTK.Button(obj, text='Tắt máy')
        obj.ScreenCapture_ = exTK.Button(obj, text='Chụp màn hình',command=ScreenShot)
        obj.Keystroke_ = exTK.Button(obj, text='Keystroke')
        obj.EditRegistry_ = exTK.Button(obj, text='Sửa Registry')
        obj.Exit_ = exTK.Button(obj, text='Thoát', command=obj.quit)
        master.bind('<Configure>', obj.placeGUI)
    def connect(obj):
        ip = str(obj.inputText.get())



def guiStart():
    win = Tk()
    win.title('Client')
    win.geometry('700x600')
    GiaoDien = monitor(win)
    GiaoDien.place(relwidth=1, relheight=1)
    win.mainloop()

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
        root = Toplevel()
        root.title('Pic')
        root.geometry('700x600')
        GiaoDien = monitor2(root)
        GiaoDien.place(relwidth=1, relheight=1)
        root.mainloop()
    guiScreen()
    
guiStart()
