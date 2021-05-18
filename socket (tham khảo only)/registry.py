import tkinter as tk
import tkinter.font as tkFont
from tkinter import ttk
import json
from setuptools.msvc import winreg
from utils import receive_data
from components import Text, Entry
from utils import hide_widget, show_widget
from tkinter import filedialog
import winreg
import subprocess
import os


class Registry:
    SZ = 'REG_SZ'
    EXPAND_SZ = 'REG_EXPAND_SZ'
    BINARY = 'REG_BINARY'
    DWORD = 'REG_DWORD'
    MULTI_SZ = 'REG_MULTI_SZ'
    QWORD = 'REG_QWORD'

    @staticmethod
    def get_value(link, name):
        hkey = link.split('\\')
        if hkey[0] != 'HKEY_CURRENT_USER' and hkey[0] != 'HKCU':
            return {'state': False, 'message': 'Lỗi'}
        hkey.pop(0)
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, '\\'.join(hkey), 0, winreg.KEY_QUERY_VALUE)
            value, datatype = winreg.QueryValueEx(key, name)
            result = {'state': True, 'message': str(value)}
            return result
        except Exception as error:
            return {'state': False, 'message': str(error)}

    @staticmethod
    def set_value(link, name, value, datatype):
        try:
            p = subprocess.run(f'reg add "{link}" /v "{name}" /t {datatype} /d {value} /f', shell=True,
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            result = {'state': False, 'message': 'Lỗi'}
            if p.stderr.decode() == '':
                result = {'state': True, 'message': 'Set value thành công'}
            return result
        except Exception as error:
            return {'state': False, 'message': str(error)}

    @staticmethod
    def delete_value(link, name):
        try:
            p = subprocess.run(f'reg delete "{link}" /v "{name}" /f', shell=True, stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
            result = {'state': False, 'message': 'Lỗi'}
            if p.stderr.decode() == '':
                result = {'state': True, 'message': 'Xoá value thành công'}
            return result
        except Exception as error:
            return {'state': False, 'message': str(error)}

    @staticmethod
    def create_key(link):
        try:
            p = subprocess.run(f'reg add "{link}" /f', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            result = {'state': False, 'message': 'Lỗi'}
            if p.stderr.decode() == '':
                result = {'state': True, 'message': 'Tạo key thành công'}
            return result
        except Exception as error:
            return {'state': False, 'message': str(error)}

    @staticmethod
    def delete_key(link):
        try:
            p = subprocess.run(f'reg delete "{link}" /f', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            result = {'state': False, 'message': 'Lỗi'}
            if p.stderr.decode() == '':
                result = {'state': True, 'message': 'Xóa key thành công'}
            return result
        except Exception as error:
            return {'state': False, 'message': str(error)}

    @staticmethod
    def import_key(content):
        try:
            with open('content.reg', 'w') as f:
                f.writelines(content)
            path = os.path.abspath('content.reg')
            p = subprocess.run(f'reg import "{path}"', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            result = {'state': False, 'message': 'Lỗi'}
            if p.stderr == b'The operation completed successfully.\r\r\n':
                result = {'state': True, 'message': 'Sửa thành công'}
            return result
        except Exception as error:
            return {'state': False, 'message': str(error)}


class RegistryUI:
    def __init__(self, parent, client):
        self.root = tk.Toplevel(parent)
        self.root.transient(parent)
        self.root.grab_set()
        # setting title
        self.root.title("registry")
        # setting window size
        width = 452
        height = 500
        screenwidth = self.root.winfo_screenwidth()
        screenheight = self.root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        self.root.geometry(alignstr)
        self.root.resizable(width=False, height=False)

        browser_btn = tk.Button(self.root)
        browser_btn["bg"] = "#efefef"
        ft = tkFont.Font(family='Times', size=10)
        browser_btn["font"] = ft
        browser_btn["fg"] = "#000000"
        browser_btn["justify"] = "center"
        browser_btn["text"] = "Browser..."
        browser_btn.place(x=340, y=30, width=100, height=30)
        browser_btn["command"] = self.browser_btn_command

        send_content = tk.Button(self.root)
        send_content["bg"] = "#efefef"
        ft = tkFont.Font(family='Times', size=10)
        send_content["font"] = ft
        send_content["fg"] = "#000000"
        send_content["justify"] = "center"
        send_content["text"] = "Gửi nội dung"
        send_content.place(x=340, y=80, width=100, height=102)
        send_content["command"] = lambda: self.send_content_command(client)

        self.file_link = Entry(self.root, "Đường dẫn ...")
        self.file_link.place(x=10, y=30, width=312, height=30)

        self.content = Text(self.root, "Nội dung", has_scroll_bar=True)
        self.content.place(x=10, y=80, w=312, h=102)

        action_frame = tk.LabelFrame(self.root, text="Sửa giá trị trực tiếp")
        action_frame.place(x=10, y=200, width=432, height=280)

        self.action_list = ttk.Combobox(self.root)
        self.action_list['values'] = (
            'Get value',
            'Set value',
            'Delete value',
            'Create key',
            'Delete key'
        )
        self.action_list.set('Chọn chức năng')
        self.action_list.bind("<<ComboboxSelected>>", self.action_list_callback)
        self.action_list.place(x=20, y=220, width=412, height=30)

        self.action_file_link = Entry(self.root, text="Đường dẫn")
        self.action_file_link.place(x=20, y=260, width=412, height=30)

        self.name_field = Entry(self.root, text="Name value")
        self.name_field_place = dict(x=20, y=300, width=130, height=25)
        show_widget(self.name_field, self.name_field_place)

        self.value_field = Entry(self.root, text="Value")
        self.value_field_place = dict(x=161, y=300, width=130, height=25)
        show_widget(self.value_field, self.value_field_place)
        self.datatype_field = ttk.Combobox(self.root)
        self.datatype_field["values"] = (
            'String',
            'Binary',
            'DWORD',
            'QWORD',
            'Multi-String',
            'Expandable String'
        )

        self.datatype_field.set('Kiểu dữ liệu')
        self.datatype_field_place = dict(x=302, y=300, width=130, height=25)
        show_widget(self.datatype_field, self.datatype_field_place)

        self.result = tk.Text(self.root)
        self.result.configure(state='disabled')
        self.result["bg"] = '#eeeeee'
        self.result.place(x=20, y=335, width=412, height=100)

        send_btn = tk.Button(self.root)
        send_btn["bg"] = "#efefef"
        ft = tkFont.Font(family='Times', size=10)
        send_btn["font"] = ft
        send_btn["fg"] = "#000000"
        send_btn["justify"] = "center"
        send_btn["text"] = "Gửi"
        send_btn.place(x=100, y=450, width=100, height=20)
        send_btn["command"] = lambda: self.send_btn_command(client)

        delete_btn = tk.Button(self.root)
        delete_btn["bg"] = "#efefef"
        ft = tkFont.Font(family='Times', size=10)
        delete_btn["font"] = ft
        delete_btn["fg"] = "#000000"
        delete_btn["justify"] = "center"
        delete_btn["text"] = "Xoá"
        delete_btn.place(x=230, y=450, width=100, height=20)
        delete_btn["command"] = self.delete_btn_command

    def action_list_callback(self, event):
        action = event.widget.get()
        if action == 'Get value':
            show_widget(self.name_field, self.name_field_place)
            hide_widget(self.value_field, self.value_field_place)
            hide_widget(self.datatype_field, self.datatype_field_place)
        elif action == 'Set value':
            show_widget(self.name_field, self.name_field_place)
            show_widget(self.value_field, self.value_field_place)
            show_widget(self.datatype_field, self.datatype_field_place)
        elif action == 'Delete value':
            show_widget(self.name_field, self.name_field_place)
            hide_widget(self.value_field, self.value_field_place)
            hide_widget(self.datatype_field, self.datatype_field_place)
        elif action == 'Create key' or action == 'Delete key':
            hide_widget(self.name_field, self.name_field_place)
            hide_widget(self.value_field, self.value_field_place)
            hide_widget(self.datatype_field, self.datatype_field_place)

    def run(self):
        self.root.mainloop()

    def browser_btn_command(self):
        filename = filedialog.askopenfilename()
        try:
            self.file_link.delete_default()
            self.file_link.clear()
            self.file_link.insert(0, filename)
            with open(filename) as f:
                content = f.readlines()
                self.content.delete_default()
                self.content.clear()
                self.content.insert(1.0, ''.join(content))
        except Exception as err:
            tk.messagebox.showerror(err)

    def send_btn_command(self, client):
        dict_type = {
            'String': Registry.SZ,
            'Binary': Registry.BINARY,
            'DWORD': Registry.DWORD,
            'QWORD': Registry.QWORD,
            'Multi-String': Registry.MULTI_SZ,
            'Expandable String': Registry.EXPAND_SZ
        }

        action = self.action_list.get()
        data = {
            'action': action,
            'address': self.action_file_link.get()
        }
        if action == 'Set value' or action == 'Get value' or action == 'Delete value':
            data['name'] = self.name_field.get()

        if action == 'Set value':
            data['value'] = self.value_field.get()
            if self.datatype_field.get() not in dict_type:
                self.insert_result('Lỗi')
                return
            data['datatype'] = dict_type[self.datatype_field.get()]

        client.send_command(cmd='registry', payload=data)
        res_data = receive_data(client, 4096)
        res_data = res_data.decode('utf-8', 'ignore')
        result = json.loads(res_data)
        self.insert_result(result['message'])

    def insert_result(self, result):
        self.result.configure(state='normal')
        self.result.insert(tk.END, result)
        self.result.configure(state='disabled')

    def delete_btn_command(self):
        self.result.configure(state='normal')
        self.result.delete(1.0, tk.END)
        self.result.configure(state='disabled')

    def send_content_command(self, client):
        data = {
            'action': 'Import key',
            'content': self.content.get(1.0, tk.END)
        }
        client.send_command(cmd='registry', payload=data)
        res_data = receive_data(client, 4096)
        res_data = res_data.decode('utf-8', 'ignore')
        result = json.loads(res_data)
        if result['state'] == 'success':
            tk.messagebox.showinfo('', result['message'])
        else:
            tk.messagebox.showerror('', result['message'])
