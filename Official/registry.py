import subprocess
import os
import winreg


def format(data):
    data = data.split('\n', 1)
    data = data[0]
    return data


def import_filereg(data):
    try:
        with os.open('tmp.reg', 'w') as file:
            file.write(data)
            a = subprocess.Popen('reg import tmp.reg', shell=True,
                                 stdout=subprocess.PIPE)
            os.remove('tmp.reg')
            return True
    except:
        return False


def getValue(data, name):
    try:
        data = data.split('\\', 1)
        data1 = str(data[0])
        data2 = str(data[1])
        data2 = format(data2)
        name = format(str(name))
        with winreg.OpenKey(getattr(winreg, data1), data2, 0, winreg.KEY_ALL_ACCESS) as registry_key:
            name = str(name)
            value, regtype = winreg.QueryValueEx(registry_key, name)
            winreg.CloseKey(registry_key)
            return value
    except WindowsError:
        return 'Lỗi'


def setValue(data, name, value, type_):
    try:
        data = data.split('\\', 1)
        data1 = str(data[0])
        data2 = str(data[1])
        data2 = format(data2)
        name = format(str(name))
        value = format(str(value))
        type_ = format(str(type_))
        winreg.CreateKey(getattr(winreg, data1), data2)
        registry_key = winreg.OpenKey(getattr(winreg, data1), data2, 0,
                                      winreg.KEY_WRITE)
        if str(type_) == 'String':
            winreg.SetValueEx(registry_key, name, 0, winreg.REG_SZ, value)
        elif str(type_) == 'Binary':
            winreg.SetValueEx(registry_key, name, 0, winreg.REG_BINARY, value)
        elif str(type_) == 'DWORD':
            winreg.SetValueEx(registry_key, name, 0, winreg.REG_DWORD, value)
        elif str(type_) == 'QWORD':
            winreg.SetValueEx(registry_key, name, 0, winreg.REG_QWORD, value)
        elif str(type_) == 'Multi-String':
            winreg.SetValueEx(registry_key, name, 0,
                              winreg.REG_MULTI_SZ, value)
        elif str(type_) == 'Expandable String':
            winreg.SetValueEx(registry_key, name, 0,
                              winreg.REG_EXPAND_SZ, value)
        else:
            return 'Lỗi'
        winreg.CloseKey(registry_key)
        return 'Set value thành công'
    except WindowsError:
        return 'Lỗi'


def deleteValue(data, name):
    try:
        data = data.split('\\', 1)
        data1 = str(data[0])
        data2 = str(data[1])
        data2 = format(data2)
        name = format(str(name))
        registry_key = winreg.OpenKey(
            getattr(winreg, data1), data2, 0, winreg.KEY_WRITE)
        winreg.DeleteValue(registry_key, name)
        winreg.CloseKey(registry_key)
        return 'Xoá value thành công'
    except WindowsError:
        return 'Lỗi'


def createKey(data):
    try:
        data = data.split('\\', 1)
        data1 = str(data[0])
        data2 = str(data[1])
        data2 = format(data2)
        registry_key = winreg.CreateKeyEx(
            getattr(winreg, data1), data2, 0, winreg.KEY_ALL_ACCESS)
        winreg.CloseKey(registry_key)
        return 'Tạo key thành công'
    except WindowsError:
        return 'Lỗi'


def deleteKey(data):
    try:
        data = data.split('\\', 1)
        data1 = str(data[0])
        data2 = str(data[1])
        data2 = format(data2)
        registry_key = winreg.DeleteKeyEx(
            getattr(winreg, data1), data2, winreg.KEY_WOW64_64KEY, 0)
        winreg.CloseKey(registry_key)
        return 'Xoá key thành công'
    except WindowsError:
        return 'Lỗi'
