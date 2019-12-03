from sendAndroid import *
from adb import *
import random
from emulate import Emulate
from NdefGeneration import *
import argparse
import re


def send(usb, data):
    if SendToAndroid(usb, data).send():
        return True
    return False


def emulationMode(payload, ndef, fuzz, log, fuzzfields):
    if log :
        ad = adb(host="127.0.0.1", port=5037)
        device = ad.ListDevices()
        if device :
            ad.logCat(device, payload)
            data = ndef.getNdef_payload(payload, fuzz, fuzzfields)
            emul = Emulate("tty:USB0")
            ad.logCat(device, payload)
            emul.emulate(data)
            ad.logCat(device, payload)

            ad.close_logcat()
        else:
            print("No such devices")
    else:
        data = ndef.getNdef_payload(payload, fuzz, fuzzfields)
        emul = Emulate("tty:USB0")
        emul.emulate(data)

def fuzz(ndef,payload):

    mutated_sample = mutate(bytearray(payload.encode()))
    #
    print("mutated_sample", mutated_sample)
    print("mutated_sample type", type(mutated_sample))
    emul = Emulate("tty:USB0")
    emul.emulate(mutated_sample)

def normalMode(payload):
    ad = adb(host="127.0.0.1", port=5037)
    device = ad.ListDevices()
    input_samples = mutate(bytearray(payload.encode()))

    ad.logCat(device, payload)
    send("tty:USB0", payload)
    ad.logCat(device, payload)
    mutated_sample = mutate(random.choice(input_samples))
    ad.logCat(device, mutated_sample.decode('ISO-8859-1'))
    send("tty:USB0", mutated_sample.decode('ISO-8859-1'))
    ad.logCat(device, mutated_sample.decode('ISO-8859-1'))

def __init__():
    ndef = NdefGeneration()
    ad = adb(host="127.0.0.1", port=5037)

    parser = argparse.ArgumentParser()

    parser.add_argument("-p", type=str, help="Payload")

    parser.add_argument("-emulate",
                    help="Emulation Mode : -emulate payload", action='store_true')

    parser.add_argument("-normal",
                    help="None emulation Mode : -normal payload", action='store_true')

    parser.add_argument("-fuzz", help="Fuzz a payload : -fuzz payload", action='store_true')

    parser.add_argument("-field", type=str, help="Fuzz field field in ndef format : -field paylod")

    parser.add_argument("-adb", help="Log from android smartphone", action='store_true')
    results = parser.parse_args()



    if not results.p :
        print("Need payload : python __init__.py -p Payload")
        exit(0)

    if results.emulate :
        emulationMode(results.p, ndef, 0, 0, 0)


    if results.normal:
        normalMode(results.p)

    if results.fuzz and results.adb :
        emulationMode(results.p, ndef, 1, 1, 0)

    if results.fuzz :
        emulationMode(results.p, ndef, 1, 0, 0)

    if results.adb :
        emulationMode(results.p, ndef, 0, 1, 0)

    if results.field :
        if re.search("TNF", results.field):
            ndef.setRandTNF()
        elif re.search("MB", results.field):
            ndef.setRandMB()
        elif re.search("ME", results.field):
            ndef.setRandME()
        elif re.search("CR", results.field):
            ndef.setRandCR()
        elif re.search("SR", results.field):
            ndef.setRandSR()
        elif re.search("IL", results.field):
            ndef.setRandIL()
        else:
            print("Invalid field ! You can only fuzz one of them : [TNF, MB, ME, CR, SR, IL]")
            exit(0)
        if results.adb :
            emulationMode(results.p, ndef, 0, 0, 1)
        else:
            emulationMode(results.p, ndef, 0, 1, 1)


__init__()
