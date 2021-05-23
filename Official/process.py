import os
import signal
import psutil
import subprocess

def getListProcess():
    try:
        procs = []
        for proc in psutil.process_iter():
            with proc.oneshot():
                info = {}
                info['name'] = proc.name()
                info['id'] = proc.pid
                info['count_threads'] = proc.num_threads()
                procs.append(info)
        return procs
    except:
        return []


def startProcess(process_name):
    os.system('start ' + process_name)


def killProcess(pid):
    os.kill(int(pid), signal.SIGTERM)

def getListApp():
        try:
            cmd = 'powershell "gps | where {$_.MainWindowTitle } | select Id'
            proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
            pids = []
            for line in proc.stdout:
                try:
                    pids.append(int(line.decode().rstrip()))
                except ValueError:
                    pass
            apps = []
            for pid in pids:
                try:
                    proc = psutil.Process(pid)
                    with proc.oneshot():
                        info = {}
                        info['name'] = proc.name()
                        info['id'] = proc.pid
                        info['count_threads'] = proc.num_threads()
                        apps.append(info)
                except psutil.NoSuchProcess:
                    pass
            return apps
        except:
            return []