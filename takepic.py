from tkinter import *
import tkinter.ttk as exTK
from tkinter import filedialog
import pyautogui
import pickle
from PIL import ImageTk, Image


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
            obj.panel.place(x=270, y=200, anchor="center")

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
    win = Tk()
    win.title('Pic')
    win.geometry('700x400')
    GiaoDien = monitor2(win)
    GiaoDien.place(relwidth=1, relheight=1)
    win.mainloop()


guiScreen()
