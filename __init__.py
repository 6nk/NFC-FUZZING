from mFuzz import *
from sendAndroid import *
from adb import *
import random
from emulate import Emulate
from NdefGeneration import *
import argparse


def send(usb, data):
    if SendToAndroid(usb, data).send():
        return True
    return False


def emulationMode():
    # ad = adb(host="127.0.0.1", port=5037)
    # device = ad.ListDevices()
    # data =  load_file("data/data/")

    ndef = NdefGeneration()
    data = ndef.getNdef_payload("www.google.com")
    emul = Emulate("tty:USB0")
    # data = "http://www.google.com"
    # ad.logCat(device, data)
    emul.emulate(data)
    # print("NDEF TNF ", ndef.getTNF())
    # ad.logCat(device, data)

    # mutated_sample = mutate((data))
    #
    # print("mutated_sample", mutated_sample)
    # print("mutated_sample type", type(mutated_sample))
    # # ad.logCat(device, mutated_sample.decode('ISO-8859-1'))
    # emul.emulate(mutated_sample)
    # ad.logCat(device, mutated_sample.decode('ISO-8859-1'))


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

    parser = argparse.ArgumentParser()
    parser.add_argument("square", type=int,
                        help="display a square of a given number")
    parser.add_argument("-v", "--verbose", action="store_true",
                        help="increase output verbosity")
    args = parser.parse_args()
    answer = args.square**2
    if args.verbose:
        print("the square of {} equals {}".format(args.square, answer))
    else:
        print(answer)





__init__()
