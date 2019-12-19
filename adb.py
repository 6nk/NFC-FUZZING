from ppadb.client import Client as AdbClient
import uuid
import subprocess
import os
import logging

class adb:
    """
        The purpose of this class is to establish the connection between
        the computer and the smartphone, to get the log files.
    """
    def __init__(self, host, port):
        """
            Default host is "127.0.0.1" and Default port is 5037
        """
        self.host = host
        self.port = port
        data = None
        self.connect = None

    def connectServer(self):
        """
            Method to establish a connection between smartphone and computer.
        """
        client = AdbClient(host=self.host, port=self.port)
        if client :
            print("Client version :", client.version())
            return client
        else:
            print("Problem to connect adb Server, please verify your port or host")

    def ListDevices(self):
        """
            Method to get the list of smartphones connected to the computer.
        """
        devices = subprocess.check_output(['adb', 'devices'])
        devices = devices.decode("utf-8").replace("List of devices attached", "")
        devices = devices.replace("device","").replace(os.linesep, "")
        return devices.strip()

    def connectDevice(self, deviceName):
        """
            Connect the smartphone to the ADB server

            Parameter : smartphone deviceName or smartphone device id
        """
        client = self.connectServer()
        device = client.device(deviceName)
        return device

    def dump_logcat(self, connect):
        """
            Capture 100 lines of smartphone logs
            And store it in a file
        """
        self.connect = connect.socket.makefile()
        for index in range(0, 100):
            print("Data {}: {}".format(self.getData(), self.connect.readline().strip()))
            self.save_to_file("emlog.log", "Data {}: {} \r\n".format(self.getData(), self.connect.readline().strip()))

    def close_logcat(self):
        """
            Close the connection to the server.
        """
        self.connect.close()

    def setData(self, data):
        self.data = data

    def getData(self):
        return self.data

    def reboot(self, deviceName):
        """
            Reboot the smartphone according to its deviceName
        """
        device = self.connectDevice(deviceName)
        device.shell("reboot")

    def save_to_file(self, fname,data):
        """
            Save log to a file
            Parameter :
                fname : file Name
                data : log data
        """
        with open(fname, "a+") as file:
            file.write(data)
            file.close()

    def logCat(self, deviceName, data):
        """
            Capture only error logcat of the smartphone
        """
        self.setData(data)
        device = self.connectDevice(deviceName)
        device.shell("logcat logcat *:E", handler=self.dump_logcat)

    def screenshot(self, deviceName):
        """
            Permit to take a screenshot of the smartphone according to its deviceName
        """
        device = self.connectDevice(deviceName)
        result = device.screencap()
        filename = str(uuid.uuid4().hex)
        with open(filename+".jpg", "wb") as fp:
            fp.write(result)
            fp.close()
