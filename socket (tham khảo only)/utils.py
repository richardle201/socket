import socket
import struct
from tkinter import messagebox


def catch_socket_error(func):
    def run_function(ref, *args, **kwargs):
        try:
            func(ref, *args, **kwargs)
        except socket.error as err:
            messagebox.showerror('', err)
        except Exception as e:
            messagebox.showerror('', e)
        finally:
            print("Unexpected error!")
    return run_function


def hide_widget(widget, place_parameters: dict):
    widget.place(x=place_parameters['x'], y=place_parameters['y'], width=0, height=0)


def show_widget(widget, place_parameters: dict):
    widget.place(**place_parameters)


def send_data(conn, data: bytes):
    size = len(data)
    conn.send(struct.pack(">L", size))
    conn.send(data)


def receive_data(conn, buffer):
    """
    :param conn: socket connection
    :param buffer: buffer size
    """
    payload_size = struct.calcsize(">L")
    payload = conn.recv(payload_size)
    if len(payload) == 0:
        return payload
    packed_msg_size = payload[:payload_size]
    msg_size = struct.unpack(">L", packed_msg_size)[0]
    data = b''
    size = len(data)
    while size < msg_size:
        chunk = conn.recv(min(msg_size - size, buffer))
        data += chunk
        size += len(chunk)
    return data


def check_connect(function):
    def run_function(ref, *args, **kwargs):
        if ref.client is None or not ref.client.is_connected():
            messagebox.showerror('', "Chưa kết nối đến server")
            return
        function(ref, *args, **kwargs)
    return run_function

