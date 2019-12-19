from __future__ import print_function

import subprocess
import random
import struct
import os


count_bit = 0
count_byte = 0
count_magic = 0

def load_file(path):
    """
        Load dataset from a file
    """
    fname = path+random.choice(os.listdir(path))
    with open(fname, "rb") as file :
        read = file.read()
        file.close()
        return bytearray(read)

def save_file(fname, data):
    """
        Save bytearray to a file
    """
    with open(fname, "wb") as file:
        file.write(str(data).replace("bytearray(b'", "").replace("')", "").replace('\\', "").encode())
        file.close()

def mutate_bits(data, rate):
    """
        Mutate randomly X% bits of a data bytearray
    """
    global count_bit
    count_bit +=1
    print("mutate_bits")
    count = int((len(data) * 8)*rate/100) # how much % we want to mutate (10% here)
    if count == 0 :
        count = 1
    for i in range(count):
        bit = random.randint(0, len(data)*8-1)
        idx_bit = bit%8
        idx_byte = bit/8
        data[int(idx_byte)] ^= 1 << idx_bit
    return data

def mutate_bytes(data, rate):
    """
        Mutate randomly X% bytes of a data bytearray
    """
    global count_byte
    count_byte += 1
    print("mutate_bytes")
    count = int(len(data)*rate/100) # how much % we want to mutate
    if count == 0 :
        count = 1
    for i in range(count):
        rand = random.randint(0,255)
        x = random.randint(0, len(data) - 1)
        data[x]  = rand
    return data

def mutate_magic(data, rate):
    """
        Replace randomly X% of a data bytearray by specific bytes
    """
    global count_magic
    count_magic += 1
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
    if count == 0 :
        count = 1
    for i in range(count):
        n_size, n = random.choice(numbers)
        size = len(data) - n_size
        if size > 0 :
            idx = random.randint(0, size)
            data[idx:idx + n_size] = bytearray(n)

    return data

def loopNumbers():
    """
        Print the number of occurrences of each mutation algorithm.
    """
    print("Bit mutation ", count_bit)
    print("Byte mutation ", count_byte)
    print("Magic mutation ", count_magic)

def mutate(data, rate):
    """
        Choose randomly the mutation algorithm to use
    """
    return random.choice([
        mutate_bits,
        mutate_bytes,
        mutate_magic
       ])(data[::], rate)
