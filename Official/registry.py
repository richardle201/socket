import subprocess
import os
import winreg
import ctypes


def import_filereg(data):
    try:
        with open('tmp.reg', 'w') as file:
            file.write(data)
            subprocess.Popen('reg import tmp.reg', shell=True,
                             stdout=subprocess.PIPE)
            os.remove('tmp.reg')
            return True
    except:
        return False


def getValue(data, name):
    try:
        data = data.split('\\',1)
        data1 = str(data[0])
        data2 = str(data[1])
        print (data1)
        print (data2)
        if data1 == 'HKEY_CURRENT_USER':
            print(1)
            registry_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, data2, 0,
                                          winreg.KEY_READ)
        else:
            return None
        name = str(name)
        print(2)
        value, regtype = winreg.QueryValueEx(registry_key, name)
        print(3)
        winreg.CloseKey(registry_key)
        return value
    except WindowsError:
        print(4)
        return None