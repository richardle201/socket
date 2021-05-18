import socket
import threading
import tkinter as tk
import tkinter.font as tkFont
from screenshot import Screenshot
from utils import catch_socket_error, send_data, receive_data, check_connect
from keystroke import KeystrokeUI
from process import CheckProcessUI, CheckAppUI
from registry import RegistryUI
from tkinter import messagebox
import json


class Client:
    def __init__(self, host_ip, port):
        self.s = socket.socket()
        t = threading.Thread(target=self.connect, args=[host_ip, port])
        t.start()

    def connect(self, host_ip, port):
        try:
            # connect to the server on local computer
            self.s.connect((host_ip, port))
            messagebox.showinfo('', 'Kết nối đến server thành công!')
        except socket.error as err:
            messagebox.showerror('', "Lỗi kết nối đến server")

    def close(self):
        self.s.close()

    def is_connected(self):
        try:
            self.send_command('check_connect')
            data = receive_data(self.s, 2048)
            if data.decode('utf-8') == 'connected':
                return True
        except socket.error:
            self.s.close()
            self.s = socket.socket()
            return False

    def recv(self, size):
        return self.s.recv(size)

    def get_socket_state(self):
        return self.s.__getstate__

    def send_command(self, cmd: str,  payload: str = ''):
        data = {
            'cmd': cmd,
            'payload': payload
        }
        data = json.dumps(data)
        send_data(self.s, bytes(data, encoding='utf-8'))


class App:
    def __init__(self, root):
        root.title("Client")
        # setting window size
        width = 424
        height = 308
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        root.geometry(alignstr)
        root.resizable(width=False, height=False)

        self.entry_ip = tk.Entry(root)
        self.entry_ip["borderwidth"] = "1px"
        ft = tkFont.Font(family='Times', size=10)
        self.entry_ip["font"] = ft
        self.entry_ip["fg"] = "#333333"
        self.entry_ip["justify"] = "center"
        self.entry_ip["text"] = "Nhập IP"
        self.entry_ip.place(x=30, y=30, width=253, height=30)

        btn_connect = tk.Button(root, relief='raised')
        btn_connect["bg"] = "#efefef"
        ft = tkFont.Font(family='Times', size=10)
        btn_connect["font"] = ft
        btn_connect["fg"] = "#000000"
        btn_connect["justify"] = "center"
        btn_connect["text"] = "Kết nối"
        btn_connect.place(x=300, y=30, width=88, height=30)
        btn_connect["command"] = self.btn_connect_command

        check_process = tk.Button(root)
        check_process["bg"] = "#efefef"
        ft = tkFont.Font(family='Times', size=10)
        check_process["font"] = ft
        check_process["fg"] = "#000000"
        check_process["justify"] = "center"
        check_process["text"] = "Process\nRunning"
        check_process.place(x=30, y=80, width=90, height=196)
        check_process["command"] = lambda: self.check_process_command(root)

        check_app = tk.Button(root)
        check_app["bg"] = "#efefef"
        ft = tkFont.Font(family='Times', size=10)
        check_app["font"] = ft
        check_app["fg"] = "#000000"
        check_app["justify"] = "center"
        check_app["text"] = "App Running"
        check_app.place(x=130, y=80, width=150, height=61)
        check_app["command"] = lambda: self.check_app_command(root)

        shutdown = tk.Button(root)
        shutdown["bg"] = "#efefef"
        ft = tkFont.Font(family='Times', size=10)
        shutdown["font"] = ft
        shutdown["fg"] = "#000000"
        shutdown["justify"] = "center"
        shutdown["text"] = "Tắt\nmáy"
        shutdown.place(x=130, y=150, width=50, height=62)
        shutdown["command"] = self.shutdown_command

        screenshot = tk.Button(root)
        screenshot["bg"] = "#efefef"
        ft = tkFont.Font(family='Times', size=10)
        screenshot["font"] = ft
        screenshot["fg"] = "#000000"
        screenshot["justify"] = "center"
        screenshot["text"] = "Chụp màn hình"
        screenshot.place(x=190, y=150, width=90, height=62)
        screenshot["command"] = self.screenshot_command

        change_register = tk.Button(root)
        change_register["bg"] = "#efefef"
        ft = tkFont.Font(family='Times', size=10)
        change_register["font"] = ft
        change_register["fg"] = "#000000"
        change_register["justify"] = "center"
        change_register["text"] = "Sửa registry"
        change_register.place(x=130, y=220, width=201, height=56)
        change_register["command"] = lambda: self.change_register_command(root)

        keystroke = tk.Button(root)
        keystroke["bg"] = "#efefef"
        ft = tkFont.Font(family='Times', size=10)
        keystroke["font"] = ft
        keystroke["fg"] = "#000000"
        keystroke["justify"] = "center"
        keystroke["text"] = "Keystroke"
        keystroke.place(x=290, y=80, width=98, height=132)
        keystroke["command"] = self.keystroke_command

        exit_btn = tk.Button(root)
        exit_btn["bg"] = "#efefef"
        ft = tkFont.Font(family='Times', size=10)
        exit_btn["font"] = ft
        exit_btn["fg"] = "#000000"
        exit_btn["justify"] = "center"
        exit_btn["text"] = "Thoát"
        exit_btn.place(x=340, y=220, width=48, height=55)
        exit_btn["command"] = lambda: self.exit_btn_command(root)
        self.client = None

    def btn_connect_command(self):
        # Define the port on which you want to connect
        host_ip = self.entry_ip.get()
        port = 9000
        self.client = Client(host_ip, port)

    @check_connect
    def check_process_command(self, root):
        check_process = CheckProcessUI(root, self.client)
        check_process.run()

    @check_connect
    def check_app_command(self, root):
        check_app = CheckAppUI(root, self.client)
        check_app.run()

    @check_connect
    def shutdown_command(self):
        self.client.send_command('shutdown')

    @check_connect
    @catch_socket_error
    def screenshot_command(self):
        screenshot_tk = Screenshot(self.client)

    @check_connect
    @catch_socket_error
    def change_register_command(self, root):
        registry_tk = RegistryUI(root, self.client)
        registry_tk.run()

    @check_connect
    @catch_socket_error
    def keystroke_command(self):
        keystroke = KeystrokeUI(self.client)
        keystroke.run()

    def exit_btn_command(self, root):
        if self.client is not None and self.client.is_connected():
            self.client.send_command('exit')
            self.client.close()
        root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    t = threading.Thread(target=root.mainloop)
    t.run()
