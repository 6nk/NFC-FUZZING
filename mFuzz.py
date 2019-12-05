from __future__ import print_function

import subprocess
import random
import struct
import os

def load_file(path):
    fname = path+random.choice(os.listdir(path))

    with open(fname, "rb") as file :
        read = file.read()
        file.close()
        # print(bytearray(read))
        return bytearray(read)


def save_file(fname, data):
    with open(fname, "wb") as file:
        file.write(str(data).replace("bytearray(b'", "").replace("')", "").replace('\\', "").encode())
        file.close()

def mutate_bits(data, rate):
    print("mutate_bits")
    count = int((len(data) * 8)*rate/100) # how much % we want to mutate (10% here)
    # print(("data length", len(data)))
    # print(("Number of mutation", count))
    if count == 0 :
        count = 1
    for i in range(count):
        print(("--------------- ITERATION ------------", i))
        bit = random.randint(0, len(data)*8-1)
        # print(("bit", bit))
        idx_bit = bit%8
        # print(("idx_bit", idx_bit))
        idx_byte = bit/8
        # print(("idx_byte", idx_byte))
        # print(("initial data", data))
        # print(("mutated idx data", data[int(idx_byte)]))
        data[int(idx_byte)] ^= 1 << idx_bit
        # print(("data", data))
    return data

def mutate_bytes(data, rate):
    print("mutate_bytes")
    count = int(len(data)**rate/100) # how much % we want to mutate
    # print(("data length", len(data)))
    # print(("Number of mutation", count))
    if count == 0 :
        count = 1
    for i in range(count):
        # print(("--------------- ITERATION ------------", i))
        # print(("data initial", data))
        rand = random.randint(0,255)
        x = random.randint(0, len(data) - 1)
        # print(('x', x))
        # print(("random value", rand))
        data[x]  = rand
        # print(("data", data))
    return data

def mutate_magic(data, rate):
    print("mutate_magic")
    numbers = [
        (1, struct.pack("B", 0xff)),
        (1, struct.pack("B", 0x7f)),
        (1, struct.pack("B", 0)),
        (2, struct.pack("H", 0xffff)),
        (2, struct.pack("H", 0)),
        (4, struct.pack("I", 0xffffffff)),
        (4, struct.pack("I", 0)),
        (4, struct.pack("I", 0x80000000)),
        (4, struct.pack("I", 0x7fffffff)),
        ]
    count = int(len(data) *rate/100)
    # print(("data length", len(data)))
    # print(("Number of mutation", count))
    if count == 0 :
        count = 1
    for i in range(count):
        # print(("--------------- ITERATION ------------", i))
        n_size, n = random.choice(numbers)
        # print(("nzise, n", n_size, n))
        size = len(data) - n_size
        # print(("size", size))
        if size < 0 :
            continue
        idx = random.randint(0, size)
        # print(("index", idx))
        # print(("bytearray", bytearray(n)))
        # print(("data init", data))
        # print(("data idx", data[idx:idx + n_size]))
        data[idx:idx + n_size] = bytearray(n)
        # print(("data", data))
    return data


def mutate(data, rate):
    print(type(data))
    return random.choice([
        mutate_bits,
        mutate_bytes,
        mutate_magic
       ])(data[::], rate)
