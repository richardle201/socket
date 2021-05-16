import subprocess
import os
import signal

def getListProcess():
    output = os.popen(
        'powershell "gps | select name, id, {$_.Threads.Count}').read()
    return output
print(getListProcess())

def start(process_name):
    os.system('start ' + process_name)


def kill(pid):
    os.kill(int(pid), signal.SIGTERM)

def getlistApp():
    cmd = 'powershell "gps | where {$_.MainWindowTitle } | select Description , Id, {$_.Threads.Count}'
    proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    data = []
    for line in proc.stdout:
        data.append(line.decode().rstrip())
    return data
# demo
# a=getlistApp()
# for i in a:
#     print(i)
