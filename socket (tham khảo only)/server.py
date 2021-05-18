import os
import socket
import threading
import tkinter as tk
import tkinter.font as tkFont
from PIL import ImageGrab
from io import BytesIO
from utils import send_data, receive_data
from keystroke import KeystrokeManager
from process import Process, Application
from registry import Registry
import json
host_ip = ''
port = ''
s = None


class Server:
    def __init__(self):
        try:
            self.host_ip = socket.gethostbyname(socket.gethostname())
            self.port = 9000
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except socket.error as err:
            print('Error when creating socket: {}'.format(err))

    def bind_socket(self):
        try:
            self.s.bind((self.host_ip, self.port))
            self.s.listen(1)
            # means that 1 connections are kept waiting(non-accept()) if the server is busy and
            # if a 2th socket trys to connect then the connection is refused
            print("socket is listening on {}: port{}".format(self.host_ip, self.port))
        except socket.error as err:
            print('Error when binding socket: {}'.format(err))

    def initial_workers(self):
        """
            Create thread for waiting connection from client
        """
        accept_thread = threading.Thread(target=self.accept_connection)
        # shutdown this thread immediately when the program exits
        accept_thread.daemon = True
        # if not the program will wait for those threads to complete before it terminates.
        accept_thread.start()

    def accept_connection(self):
        while True:
            conn, addr = self.s.accept()
            print('Connection has been established! IP: {} | Port: {}'.format(*addr))
            serve_thread = threading.Thread(target=self.receive_command, args=[conn])
            serve_thread.daemon = True
            serve_thread.start()

    @staticmethod
    def send_response(conn, state, message):
        """
        send response to client
        :param conn: current socket connect
        :param state: Bool - result of action
        :param message: Str - message from server
        :return: None
        """
        data = {
            'state': state,
            'message': message
        }
        data = json.dumps(data)
        send_data(conn, bytes(data, encoding='utf-8'))

    def receive_command(self, conn):
        keystroke = KeystrokeManager()
        SUCCESS = 'success'
        FAILED = 'failed'
        while True:
            try:
                data = receive_data(conn, 1024)
                if len(data) == 0:
                    break
                data = data.decode('utf-8')
                data = json.loads(data)
                cmd = data['cmd']
                payload = data['payload']
                if cmd == 'check_connect':
                    send_data(conn, 'connected'.encode('utf-8'))
                elif cmd == 'screenshot':
                    screenshot = ImageGrab.grab()
                    image_bytes = BytesIO()
                    screenshot.save(image_bytes, format='PNG')
                    image = image_bytes.getvalue()
                    send_data(conn, image)
                elif cmd == 'hook':
                    keystroke.hook_key()
                elif cmd == 'unhook':
                    keystroke.unhook_key()
                elif cmd == 'get_hooked':
                    send_data(conn, keystroke.hooked_keys())
                elif cmd == 'process':
                    data = Process.view_process()
                    data = data.encode('utf-8')
                    send_data(conn, data)
                elif cmd == 'kill_process':
                    result = Process.kill_process(payload)
                    if result:
                        Server.send_response(conn, SUCCESS, message="Đã diệt process")
                    else:
                        Server.send_response(conn, FAILED, message='Không tìm thấy process này')
                elif cmd == 'start_process':
                    result = Process.start_process(payload)
                    if result:
                        Server.send_response(conn, SUCCESS, message="Process đã được bật")
                    else:
                        Server.send_response(conn, FAILED, message='Không tìm thấy process này')
                elif cmd == 'app':
                    data = Application.view_app()
                    data = data.encode('utf-8')
                    send_data(conn, data)
                elif cmd == 'kill_app':
                    result = Application.kill_app(payload)
                    if result:
                        Server.send_response(conn, SUCCESS, message="Đã diệt chương trình")
                    else:
                        Server.send_response(conn, FAILED, message="Không tìm thấy chương trình")
                elif cmd == 'start_app':
                    result = Application.start_app(payload)
                    if result:
                        Server.send_response(conn, SUCCESS, message="Chương trình đã được bật")
                    else:
                        Server.send_response(conn, FAILED, message="Không tìm thấy chương trình")

                elif cmd == 'registry':
                    if payload['action'] == 'Get value':
                        result = Registry.get_value(payload['address'], payload['name'])
                        Server.send_response(conn, SUCCESS if result['state'] else FAILED, message=result['message'])
                    elif payload['action'] == 'Set value':
                        result = Registry.set_value(payload['address'], payload['name'], payload['value'], payload['datatype'])
                        Server.send_response(conn, SUCCESS if result['state'] else FAILED, message=result['message'])
                    elif payload['action'] == 'Delete value':
                        result = Registry.delete_value(payload['address'], payload['name'])
                        Server.send_response(conn, SUCCESS if result['state'] else FAILED, message=result['message'])
                    elif payload['action'] == 'Create key':
                        result = Registry.create_key(payload['address'])
                        Server.send_response(conn, SUCCESS if result['state'] else FAILED, message=result['message'])
                    elif payload['action'] == 'Delete key':
                        result = Registry.delete_key(payload['address'])
                        Server.send_response(conn, SUCCESS if result['state'] else FAILED, message=result['message'])
                    elif payload['action'] == 'Import key':
                        result = Registry.import_key(payload['content'])
                        Server.send_response(conn, SUCCESS if result['state'] else FAILED, message=result['message'])
                    else:
                        Server.send_response(conn, FAILED, message='Lỗi')

                elif cmd == 'shutdown':
                    os.system("shutdown /s /t 1")

                elif cmd == 'exit':
                    conn.close()
                    break

            except socket.error as err:
                conn.close()
                break
        conn.close()


class App:
    def __init__(self, root):
        self.server = Server()
        root.title = 'Server'
        btn = tk.Button(root)
        btn['text'] = 'Mở server'
        btn["bg"] = "#efefef"
        ft = tkFont.Font(family='Times', size=10)
        btn["font"] = ft
        btn["fg"] = "#000000"
        btn["justify"] = "center"
        btn['command'] = self.run_server
        btn['height'] = 4
        btn['width'] = 20
        btn.pack()

    def run_server(self):
        self.server.bind_socket()
        self.server.initial_workers()


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()

