from tkinter import *
import tkinter.ttk as exTK
from tkinter import filedialog
import pyautogui


class monitor2(Frame):
    def placeGUI(obj, e):
        if e.widget == obj:
            obj.update()
            objW = e.width
            objH = e.height
            obj.screen_.place(height=objH*0.575, width=objW *
                              0.175, x=objW*0.775, y=objH/14)
            obj.save_.place(height=objH*0.2, width=objW *
                            0.175, x=objW*0.775, y=objH*0.75)

    def __init__(obj, master):
        super().__init__(master)
        obj.screen_ = exTK.Button(obj, text='Chụp')
        obj.save_ = exTK.Button(obj, text='Lưu', command=obj.saved)
        master.bind('<Configure>', obj.placeGUI)

    def saved(obj):
        save_path = filedialog.asksaveasfilename(
            initialdir='/', title='Save As', filetypes=(('All file', '*.*'), ('Bmp file', '*.Bmp')))
        pyautogui.screenshot(save_path)


def guiScreen():
    win = Tk()
    win.title('Pic')
    win.geometry('500x400')
    GiaoDien = monitor2(win)
    GiaoDien.place(relwidth=1, relheight=1)
    win.mainloop()

