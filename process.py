import os
import signal
import psutil
import subprocess
import threading

def getListProcess():
    output = os.popen('powershell "gps | select name, id, {$_.Threads.Count}').read()
    return output

def start(process_name):
    try:
        t = threading.Thread(
            target = subprocess.Popen,
            args = [process_name],
            kwargs = {'shell':True, 'stdout':subprocess.PIPE}
        )
        t.run()
        return True
    except:
        return False


def killProcess (process_name):
    try:
        killed = os.system('tskill ' + process_name)
        return True
    except:
        return False
