from sendAndroid import *
from adb import *
import random
from emulate import Emulate
from NdefGeneration import *
import argparse
import re


def send(usb, data):
    """
        Send ndef data to an android smartphone
    """
    if SendToAndroid(usb, data).send():
        return True
    return False

def emulationMode(payload, ndef, fuzz, log, fuzzfields):
    """
        Emulate 10 NDEF message using a payload
        Can read android phone log, if log = 1
    """
    if log :
        ad = adb(host="127.0.0.1", port=5037)
        device = ad.ListDevices()
        if device :
            for i in range(10):
                ad.logCat(device, payload)
                data = ndef.getNdef_payload(payload, fuzz, fuzzfields)
                emul = Emulate("tty:USB0")
                ad.logCat(device, data)
                emul.emulate(data)
                ad.logCat(device, data)

            ad.close_logcat()
        else:
            print("No such devices")
    else:
        for i in range(10):
            data = ndef.getNdef_payload(payload, fuzz, fuzzfields)
            emul = Emulate("tty:USB0")
            emul.emulate(data)

def normalMode(payload):
    """
        Send ndef message to smartphone, without emulation
    """
    input_samples = mutate(bytearray(payload.encode()), 10)
    send("tty:USB0", payload)

def fromFile(log, loop):
    """
        Loop mode : Send X ndef messages using validated data, stored in a file
    """
    for i in range(loop):
        if log :
            ad = adb(host="127.0.0.1", port=5037)
            device = ad.ListDevices()
            if device :
                input_samples = [ load_file("data/") ]
                print("Initial data :", input_samples[0].decode("iso-8859-1"))
                mutated_sample = mutate(input_samples[0], 10)
                ad.logCat(device, mutated_sample)
                emul = Emulate("tty:USB0")

                ad.logCat(device, mutated_sample)
                emul.emulate(mutated_sample)
                ad.logCat(device, mutated_sample)
                ad.logCat(device, mutated_sample)
                ad.close_logcat()
            else:
                print("No such devices")
        else :
            input_samples = [ load_file("data/") ]
            print("Initial data :", input_samples[0].decode("iso-8859-1"))
            mutated_sample = mutate(input_samples[0], 10)
            emul = Emulate("tty:USB0")
            emul.emulate(mutated_sample)
    loopNumbers()

def __init__():
    ndef = NdefGeneration()
    ad = adb(host="127.0.0.1", port=5037)
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", type=str, help="Payload")
    parser.add_argument("-emulate", help="Emulation Mode : -emulate payload", action='store_true')
    parser.add_argument("-normal", help="None emulation Mode : -normal payload", action='store_true')
    parser.add_argument("-fuzz", help="Fuzz a payload : -fuzz payload", action='store_true')
    parser.add_argument("-field", type=str, help="Fuzz field field in ndef format : -field paylod")
    parser.add_argument("-adb", help="Log from android smartphone", action='store_true')
    parser.add_argument("-loop", type=int, help="Fuzz several time : -loop number of loops")
    parser.add_argument("-bluetooth", type=str, help='Activate bluetooth using NFC')
    results = parser.parse_args()
    if results.bluetooth:
        emulationMode(results.bluetooth, ndef, 0,0,0)
    if results.loop and results.adb:
        fromFile(1, results.loop)
    if results.loop :
        fromFile(0, results.loop)
    if not results.p :
        print("Need payload : python __init__.py -p Payload")
        exit(0)
    if results.emulate :
        emulationMode(results.p, ndef, 0, 0, 0)
    if results.normal:
        normalMode(results.p)
    if results.fuzz and results.adb :
        emulationMode(results.p, ndef, 1, 1, 0)
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
            emulationMode(results.p, ndef, 0, 1, 1)
        else:
            emulationMode(results.p, ndef, 0, 0, 1)
    elif results.fuzz :
        emulationMode(results.p, ndef, 1, 0, 0)
    elif results.adb :
        emulationMode(results.p, ndef, 0, 1, 0)
        emulationMode(results.p, ndef, 0, 1, 0)

__init__()
