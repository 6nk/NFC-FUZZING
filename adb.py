from ppadb.client import Client as AdbClient
import uuid
import subprocess
import os
import logging

class adb:

    def __init__(self, host, port):
        self.host = host
        self.port = port
        data = None

    def connectServer(self):
        client = AdbClient(host=self.host, port=self.port)
        if client :
            print("Client version :", client.version())
            return client
        else:
            print("Problem to connect adb Server, please verify your port or host")

    def ListDevices(self):
        devices = subprocess.check_output(['adb', 'devices'])
        devices = devices.decode("utf-8").replace("List of devices attached", "")
        devices = devices.replace("device","").replace(os.linesep, "")
        return devices.strip()

    def connectDevice(self, deviceName):
        client = self.connectServer()
        device = client.device(deviceName)
        return device

    def dump_logcat(self, connect):
        file_obj = connect.socket.makefile()
        for index in range(0, 100):
            print("Data {}: {}".format(self.getData(), file_obj.readline().strip()))
            self.save_to_file("emlog", "Data {}: {} \r\n".format(self.getData(), file_obj.readline().strip()))
        file_obj.close()
        connect.close()

    def setData(self, data):
        self.data = data

    def getData(self):
        return self.data

    def save_to_file(self, fname,data):
        with open(fname, "a+") as file:
            file.write(data)
            file.close()

    def logCat(self, deviceName, data):
        self.setData(data)
        device = self.connectDevice(deviceName)
        device.shell("logcat logcat *:E", handler=self.dump_logcat)

    def screenshot(self, deviceName):
        device = self.connectDevice(deviceName)
        result = device.screencap()
        filename = str(uuid.uuid4().hex)
        with open(filename+".jpg", "wb") as fp:
            fp.write(result)
            fp.close()
