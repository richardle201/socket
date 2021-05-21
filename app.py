import subprocess
import os
import signal
import tkinter as tkr
from tkinter import *
import tkinter.ttk as exTK
import psutil

# server
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
def xem():
    data = getListApp()
    i = 0
    for value in data:
        tmp = str(value['name'])
        tmp = tmp.split('.exe')
        output.insert(parent='', index=i, iid=i, values=(
            tmp[0], value['id'], value['count_threads']))
        i = i+1


def kill():
    root = tkr.Toplevel()
    root.title('Kill')
    root.geometry('450x100')
    inputText = exTK.Entry(root, font='Car 12')
    inputText.place(relheight=0.35, relwidth=0.6, relx=0.05, rely=0.25)
    inputText.insert(END, 'Nhập ID')

    def action():
        ID = inputText.get()
        killProcess(ID)
    action_ = exTK.Button(root, text='Kill', command=action).place(
        relheight=0.35, relwidth=0.25, relx=0.7, rely=0.25)
    root.mainloop()


def start():
    root = tkr.Toplevel()
    root.title('Start')
    root.geometry('450x100')
    inputText = exTK.Entry(root, font='Calibri 12')
    inputText.insert(END, 'Nhập tên')
    inputText.place(relheight=0.35, relwidth=0.6, relx=0.05, rely=0.25)

    def action():
        name = inputText.get()
        startProcess(name)
    action_ = exTK.Button(root, text='Start', command=action).place(
        relheight=0.35, relwidth=0.25, relx=0.7, rely=0.25)
    root.mainloop()


def xoa():
    global output
    for i in output.get_children():
        output.delete(i)
    win.update()


win = tkr.Tk()
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

sb = tkr.Scrollbar(win, orient=VERTICAL)
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
