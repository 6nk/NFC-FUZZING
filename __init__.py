from mFuzz import *
from sendAndroid import *
from adb import *
import random
from emulate import Emulate

def fakeemulation():
    ad = adb(host="127.0.0.1", port=5037)
    device = ad.ListDevices()
    input_samples =  load_file("data/")

    data = [str(x,'ascii', 'ignore') for x in input_samples][0]
    Emulate("tty:USB0","�TenHello World!").fakeemulate()







def send(usb, data):
    if SendToAndroid(usb, data).send():
        return True
    return False


def emulationMode():
    ad = adb(host="127.0.0.1", port=5037)
    device = ad.ListDevices()
    data =  load_file("data/")
    emul = Emulate("tty:USB0")

    print(data)

    print(type(data))
    ad.logCat(device, data)
    emul.emulate(data)
    ad.logCat(device, data)

    mutated_sample = mutate((data))

    print("mutated_sample", mutated_sample)
    print("mutated_sample type", type(mutated_sample))
    ad.logCat(device, mutated_sample.decode('ISO-8859-1'))
    emul.emulate(mutated_sample)
    ad.logCat(device, mutated_sample.decode('ISO-8859-1'))


def normalMode():
    ad = adb(host="127.0.0.1", port=5037)
    device = ad.ListDevices()
    input_samples = [ load_file("data/") ]

    data = [str(x,'ascii', 'ignore') for x in input_samples][0]

    ad.logCat(device, data)
    send("tty:USB0", data)
    ad.logCat(device, data)
    mutated_sample = mutate(random.choice(input_samples))
    ad.logCat(device, mutated_sample.decode('ISO-8859-1'))
    send("tty:USB0", mutated_sample.decode('ISO-8859-1'))
    ad.logCat(device, mutated_sample.decode('ISO-8859-1'))

def __init__():


     emulationMode()


     # normalMode()






__init__()
