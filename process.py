import os
import signal


def getListProcess():
    output = os.popen(
        'powershell "gps | select name, id, {$_.Threads.Count}').read()
    return output


def startProcess(process_name):
    os.system('start ' + process_name)


def killProcess(pid):
    os.kill(int(pid), signal.SIGTERM)
