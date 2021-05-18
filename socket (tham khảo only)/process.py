import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont
import win32api
import win32process
import subprocess
from utils import receive_data
import psutil
import json
from components import Entry


class Process:
    @staticmethod
    def kill_process(pid):
        processes = psutil.process_iter()
        try:
            pid = int(pid)
            find = False
            for proc in processes:
                if pid == proc.pid:
                    find = True
            if not find:
                return False
            handle = win32api.OpenProcess(1, False, pid)
            win32process.TerminateProcess(handle, -1)
            win32api.CloseHandle(handle)
            return True
        except Exception as err:
            return False

    @staticmethod
    def start_process(name):
        try:
            proc = subprocess.Popen(name)
            return True
        except Exception as err:
            return False

    @staticmethod
    def view_process():
        lists = psutil.process_iter()
        data = ''
        for proc in lists:
            data += f'{proc.name()},{proc.pid},{proc.num_threads()}\r\n'
        return data


class Application:
    @staticmethod
    def view_app():
        cmd = 'powershell "gps | where {$_.MainWindowTitle } | select Name, Id'
        proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        apps = []
        for line in proc.stdout:
            l = line.decode()
            if not l[0].isspace():
                p = l.split(' ')
                p = [i.replace('\r\n', '') for i in p if len(i) > 0]
                apps.append(p)
        lists = psutil.process_iter()
        apps = apps[2:]

        proc_data = dict()
        for proc in lists:
            proc_data[proc.pid] = proc.num_threads()

        list_proc = proc_data.keys()
        data = ""
        for app in apps:
            app_id = int(app[1])
            if app_id in list_proc:
                data += f'{app[0]},{app[1]},{proc_data[app_id]}\r\n'
        return data

    @staticmethod
    def kill_app(pid):
        return Process.kill_process(pid)

    @staticmethod
    def start_app(name):
        return Process.start_process(name)


class Dialog:
    def __init__(self, parent, purpose, entry_text, client, cmd):
        self.root = tk.Toplevel(parent)
        self.root.transient(parent)
        self.root.grab_set()
        self.root.title(purpose)
        width = 418
        height = 71
        screenwidth = self.root.winfo_screenwidth()
        screenheight = self.root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        self.root.geometry(alignstr)
        self.root.resizable(width=False, height=False)

        ft = tkFont.Font(family='Times', size=10)
        self.input_entry = Entry(self.root,
                                 entry_text,
                                 font=ft,
                                 fg="#333333",
                                 justify="center",
                                 borderwidth="1px")

        self.input_entry.place(x=30, y=20, width=252, height=30)
        self.input_entry.focus_set()

        select_btn = tk.Button(self.root,
                               text=purpose,
                               bg="#efefef",
                               font=ft,
                               fg="#000000",
                               justify="left")
        select_btn.place(x=300, y=20, width=80, height=30)
        select_btn["command"] = lambda: self.btn_command(client, cmd)

    def run(self):
        self.root.mainloop()

    def btn_command(self, client, cmd):
        client.send_command(cmd, self.input_entry.get())
        data = receive_data(client, 4096)
        data = data.decode('utf-8')
        result = json.loads(data)

        state = result['state']
        message = result['message']
        if state == 'success':
            tk.messagebox.showinfo('', message)
        elif state == 'failed':
            tk.messagebox.showerror('', message)


class CheckProcessUI:
    def __init__(self, parent, client):
        self.root = tk.Toplevel(parent)
        self.root.transient(parent)
        self.root.grab_set()
        self.root.title("Process")
        # setting window size
        width = 560
        height = 560
        screenwidth = self.root.winfo_screenwidth()
        screenheight = self.root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        self.root.geometry(alignstr)
        self.root.resizable(width=False, height=False)

        kill_btn = tk.Button(self.root)
        kill_btn["bg"] = "#efefef"
        ft = tkFont.Font(family='Times', size=10)
        kill_btn["font"] = ft
        kill_btn["fg"] = "#000000"
        kill_btn["justify"] = "center"
        kill_btn["text"] = "Kill"
        kill_btn.place(x=60, y=50, width=100, height=60)
        kill_btn["command"] = lambda: self.kill_btn_command(client)

        view_btn = tk.Button(self.root)
        view_btn["bg"] = "#efefef"
        ft = tkFont.Font(family='Times', size=10)
        view_btn["font"] = ft
        view_btn["fg"] = "#000000"
        view_btn["justify"] = "center"
        view_btn["text"] = "Xem"
        view_btn.place(x=170, y=50, width=100, height=60)
        view_btn["command"] = lambda: self.view_btn_command(client)

        delete_btn = tk.Button(self.root)
        delete_btn["bg"] = "#efefef"
        ft = tkFont.Font(family='Times', size=10)
        delete_btn["font"] = ft
        delete_btn["fg"] = "#000000"
        delete_btn["justify"] = "center"
        delete_btn["text"] = "Xóa"
        delete_btn.place(x=280, y=50, width=100, height=60)
        delete_btn["command"] = self.delete_btn_command

        start_btn = tk.Button(self.root)
        start_btn["bg"] = "#efefef"
        ft = tkFont.Font(family='Times', size=10)
        start_btn["font"] = ft
        start_btn["fg"] = "#000000"
        start_btn["justify"] = "center"
        start_btn["text"] = "Start"
        start_btn.place(x=390, y=50, width=100, height=60)
        start_btn["command"] = lambda: self.start_btn_command(client)

        cols = ('Name Process', 'ID Process', 'Count Thread')
        self.tree = ttk.Treeview(self.root, selectmode="browse", columns=cols, show='headings')
        self.tree.column('Name Process', minwidth=180, width=180)
        self.tree.column('ID Process', minwidth=125, width=125)
        self.tree.column('Count Thread', minwidth=125, width=125)
        for col in cols:
            self.tree.heading(col, text=col)
        self.tree.place(x=60, y=120, width=430, height=400)

        vertical_scrollbar = ttk.Scrollbar(self.tree, orient='vertical', command=self.tree.yview)
        vertical_scrollbar.pack(side='right', fill='y')
        self.tree.configure(yscrollcommand=vertical_scrollbar.set)

        self.processes = []

    def run(self):
        self.root.mainloop()

    def receive_processes(self, client):
        client.send_command(cmd='process')
        result = receive_data(client, 4096)
        data = result.decode('utf-8')
        lists = list(data.split('\r\n'))
        self.processes = [(line.split(',')) for line in lists]

    def kill_btn_command(self, client):
        kill_cmd = 'kill_process'
        kill_window = Dialog(self.root, "Kill", "Nhập ID", client, kill_cmd)

    def view_btn_command(self, client):
        self.receive_processes(client)
        self.tree.delete(*self.tree.get_children())
        self.processes.sort(key=lambda x: x[0])  # sort by name
        for proc in self.processes:
            if len(proc) == 3:
                name, id, num_threads = proc
                self.tree.insert("", "end", values=(name, id, num_threads))

    def delete_btn_command(self):
        self.tree.delete(*self.tree.get_children())

    def start_btn_command(self, client):
        start_cmd = 'start_process'
        start_window = Dialog(self.root, "start", "Nhập tên", client, start_cmd)
        start_window.run()


class CheckAppUI:
    def __init__(self, parent, client):
        self.root = tk.Toplevel(parent)
        self.root.transient(parent)
        self.root.grab_set()
        self.root.title("Application")
        # setting window size
        width = 560
        height = 560
        screenwidth = self.root.winfo_screenwidth()
        screenheight = self.root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        self.root.geometry(alignstr)
        self.root.resizable(width=False, height=False)

        kill_btn = tk.Button(self.root)
        kill_btn["bg"] = "#efefef"
        ft = tkFont.Font(family='Times', size=10)
        kill_btn["font"] = ft
        kill_btn["fg"] = "#000000"
        kill_btn["justify"] = "center"
        kill_btn["text"] = "Kill"
        kill_btn.place(x=60, y=50, width=100, height=60)
        kill_btn["command"] = lambda: self.kill_btn_command(client)

        view_btn = tk.Button(self.root)
        view_btn["bg"] = "#efefef"
        ft = tkFont.Font(family='Times', size=10)
        view_btn["font"] = ft
        view_btn["fg"] = "#000000"
        view_btn["justify"] = "center"
        view_btn["text"] = "Xem"
        view_btn.place(x=170, y=50, width=100, height=60)
        view_btn["command"] = lambda: self.view_btn_command(client)

        delete_btn = tk.Button(self.root)
        delete_btn["bg"] = "#efefef"
        ft = tkFont.Font(family='Times', size=10)
        delete_btn["font"] = ft
        delete_btn["fg"] = "#000000"
        delete_btn["justify"] = "center"
        delete_btn["text"] = "Xóa"
        delete_btn.place(x=280, y=50, width=100, height=60)
        delete_btn["command"] = self.delete_btn_command

        start_btn = tk.Button(self.root)
        start_btn["bg"] = "#efefef"
        ft = tkFont.Font(family='Times', size=10)
        start_btn["font"] = ft
        start_btn["fg"] = "#000000"
        start_btn["justify"] = "center"
        start_btn["text"] = "Start"
        start_btn.place(x=390, y=50, width=100, height=60)
        start_btn["command"] = lambda: self.start_btn_command(client)

        cols = ('Name Application', 'ID Application', 'Count Thread')
        self.tree = ttk.Treeview(self.root, selectmode="browse", columns=cols, show='headings')
        self.tree.column('Name Application', minwidth=180, width=180)
        self.tree.column('ID Application', minwidth=125, width=125)
        self.tree.column('Count Thread', minwidth=125, width=125)
        for col in cols:
            self.tree.heading(col, text=col)
        self.tree.place(x=60, y=120, width=430, height=400)
        self.processes = []

        vertical_scrollbar = ttk.Scrollbar(self.tree, orient='vertical', command=self.tree.yview)
        vertical_scrollbar.pack(side='right', fill='y')
        self.tree.configure(yscrollcommand=vertical_scrollbar.set)

    def run(self):
        self.root.mainloop()

    def receive_apps(self, client):
        client.send_command(cmd='app')
        result = receive_data(client, 4096)
        data = result.decode('utf-8')
        lists = list(data.split('\r\n'))
        self.processes = [(line.split(',')) for line in lists]

    def kill_btn_command(self, client):
        kill_cmd = 'kill_app'
        kill_window = Dialog(self.root, "Kill", "Nhập ID", client, kill_cmd)

    def view_btn_command(self, client):
        self.receive_apps(client)
        self.tree.delete(*self.tree.get_children())
        self.processes.sort(key=lambda x: x[0])  # sort by name
        for proc in self.processes:
            if len(proc) == 3:
                name, id, num_threads = proc
                self.tree.insert("", "end", values=(name, id, num_threads))

    def delete_btn_command(self):
        self.tree.delete(*self.tree.get_children())

    def start_btn_command(self, client):
        start_cmd = 'start_app'
        start_window = Dialog(self.root, "start", "Nhập tên", client, start_cmd)
